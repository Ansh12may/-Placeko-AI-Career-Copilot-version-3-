"""
Candidate Level Service

Responsible for determining the candidate's career level
based on professional experience.

Levels:

    Fresher
        ↓
    Early Career
        ↓
    Experienced
        ↓
    Senior

This service performs NO AI reasoning.
"""

import re
from datetime import date

from backend.ATS.schemas.candidate_level import (
    CandidateLevel,
)


class CandidateLevelService:

    # =========================================================
    # Internship Detection
    # =========================================================

    INTERNSHIP_KEYWORDS = [
        "intern",
        "internship",
        "trainee",
        "apprentice",
    ]

    @classmethod
    def _is_internship(
        cls,
        role: str,
    ) -> bool:
        """
        Determine whether a role is an internship/trainee role.
        """

        if not role:
            return False

        role_lower = role.lower()

        return any(
            keyword in role_lower
            for keyword in cls.INTERNSHIP_KEYWORDS
        )

    # =========================================================
    # Duration Parsing
    # =========================================================

    @staticmethod
    def _parse_duration(
        duration: str,
    ) -> float:
        """
        Convert common duration formats into years.

        Supported examples:

        6 months
        1 year
        1.5 years
        2 years 6 months
        2023 - 2025
        2023 - Present
        Jan 2023 - Jun 2025
        January 2023 - June 2025

        Returns:
            Duration in years.
        """

        if not duration:
            return 0.0

        text = duration.lower().strip()

        # Normalize different dash characters
        text = re.sub(
            r"[–—]",
            "-",
            text,
        )

        # =====================================================
        # Explicit duration
        # =====================================================

        years = 0.0
        months = 0.0

        year_match = re.search(
            r"(\d+(?:\.\d+)?)\s*"
            r"(?:years?|yrs?)",
            text,
        )

        month_match = re.search(
            r"(\d+(?:\.\d+)?)\s*"
            r"(?:months?|mos?)",
            text,
        )

        if year_match:
            years = float(
                year_match.group(1)
            )

        if month_match:
            months = float(
                month_match.group(1)
            )

        if year_match or month_match:

            return round(
                years + months / 12,
                1,
            )

        # =====================================================
        # Date range
        # =====================================================

        date_range = re.search(
            r"(?P<start_month>"
            r"jan(?:uary)?|"
            r"feb(?:ruary)?|"
            r"mar(?:ch)?|"
            r"apr(?:il)?|"
            r"may|"
            r"jun(?:e)?|"
            r"jul(?:y)?|"
            r"aug(?:ust)?|"
            r"sep(?:tember)?|"
            r"oct(?:ober)?|"
            r"nov(?:ember)?|"
            r"dec(?:ember)?"
            r")?"
            r"\s*"
            r"(?P<start_year>20\d{2})"
            r"\s*-\s*"
            r"(?P<end_month>"
            r"jan(?:uary)?|"
            r"feb(?:ruary)?|"
            r"mar(?:ch)?|"
            r"apr(?:il)?|"
            r"may|"
            r"jun(?:e)?|"
            r"jul(?:y)?|"
            r"aug(?:ust)?|"
            r"sep(?:tember)?|"
            r"oct(?:ober)?|"
            r"nov(?:ember)?|"
            r"dec(?:ember)?"
            r")?"
            r"\s*"
            r"(?P<end_year>20\d{2}|present|current)",
            text,
        )

        if date_range:

            start_year = int(
                date_range.group(
                    "start_year"
                )
            )

            end_value = date_range.group(
                "end_year"
            )

            if end_value in {
                "present",
                "current",
            }:

                end_year = date.today().year

            else:

                end_year = int(
                    end_value
                )

            # ---------------------------------------------
            # Month-aware calculation
            # ---------------------------------------------

            start_month_name = (
                date_range.group(
                    "start_month"
                )
            )

            end_month_name = (
                date_range.group(
                    "end_month"
                )
            )

            if (
                start_month_name
                and end_month_name
            ):

                month_map = {
                    "jan": 1,
                    "january": 1,
                    "feb": 2,
                    "february": 2,
                    "mar": 3,
                    "march": 3,
                    "apr": 4,
                    "april": 4,
                    "may": 5,
                    "jun": 6,
                    "june": 6,
                    "jul": 7,
                    "july": 7,
                    "aug": 8,
                    "august": 8,
                    "sep": 9,
                    "september": 9,
                    "oct": 10,
                    "october": 10,
                    "nov": 11,
                    "november": 11,
                    "dec": 12,
                    "december": 12,
                }

                start_month = month_map[
                    start_month_name
                ]

                if end_value in {
                    "present",
                    "current",
                }:

                    end_month = date.today().month

                else:

                    end_month = month_map[
                        end_month_name
                    ]

                total_months = (
                    (end_year - start_year)
                    * 12
                    + (
                        end_month
                        - start_month
                    )
                )

                return max(
                    0.0,
                    round(
                        total_months / 12,
                        1,
                    ),
                )

            # ---------------------------------------------
            # Year-only range
            # ---------------------------------------------

            return max(
                0.0,
                round(
                    end_year - start_year,
                    1,
                ),
            )

        # =====================================================
        # Single year
        # =====================================================

        single_year = re.fullmatch(
            r"20\d{2}",
            text,
        )

        if single_year:
            return 0.0

        return 0.0

    # =========================================================
    # Professional Experience
    # =========================================================

    @classmethod
    def calculate_professional_experience(
        cls,
        experience,
    ) -> float:
        """
        Calculate total professional experience.

        Internships, trainee roles, and apprenticeships
        are not counted toward professional experience.

        This is important because:

            Internship ≠ full-time professional experience
        """

        if not experience:
            return 0.0

        total_years = 0.0

        for item in experience:

            if cls._is_internship(
                item.role
            ):
                continue

            total_years += (
                cls._parse_duration(
                    item.duration or ""
                )
            )

        return round(
            total_years,
            1,
        )

    # =========================================================
    # Candidate Level
    # =========================================================

    @classmethod
    def determine_level(
        cls,
        experience,
    ) -> CandidateLevel:
        """
        Determine candidate career level.

        Classification:

        0 years
            → FRESHER

        >0 and <=2 years
            → EARLY_CAREER

        >2 and <=7 years
            → EXPERIENCED

        >7 years
            → SENIOR
        """

        years = (
            cls.calculate_professional_experience(
                experience
            )
        )

        if years <= 0:
            return CandidateLevel.FRESHER

        if years <= 2:
            return CandidateLevel.EARLY_CAREER

        if years <= 7:
            return CandidateLevel.EXPERIENCED

        return CandidateLevel.SENIOR