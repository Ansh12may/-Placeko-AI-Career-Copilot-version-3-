"""
Candidate Level Service
Responsible for determining the candidate's career level
based on professional experience with accurate interval merging for overlapping roles.

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
from typing import List, Tuple, Optional
from backend.ATS.schemas.candidate_level import CandidateLevel


class CandidateLevelService:

    # Internship Detection

    INTERNSHIP_KEYWORDS = [
        "intern",
        "internship",
        "trainee",
        "apprentice",
    ]

    MONTH_MAP = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }

    @classmethod
    def _is_internship(cls, role: str) -> bool:
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

    # Duration & Interval Parsing

    @classmethod
    def _parse_to_interval(cls, duration: str) -> Tuple[Optional[Tuple[date, date]], float]:
        """
        Parses duration text. 
        Returns tuple of ((start_date, end_date), explicit_years_fallback).
        """
        if not duration:
            return None, 0.0

        text = duration.lower().strip()
        text = re.sub(r"[–—]", "-", text)

        # 1. Parse Explicit Durations (e.g., "1.5 years", "6 months")
        year_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)", text)
        month_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:months?|mos?)", text)

        if year_match or month_match:
            years = float(year_match.group(1)) if year_match else 0.0
            months = float(month_match.group(1)) if month_match else 0.0
            return None, years + (months / 12)

        # 2. Parse Date Ranges (e.g., "Jan 2020 - Dec 2022", "2021 - Present")
        date_range = re.search(
            r"(?P<start_month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)?"
            r"\s*(?P<start_year>20\d{2})"
            r"\s*-\s*"
            r"(?P<end_month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)?"
            r"\s*(?P<end_year>20\d{2}|present|current)",
            text,
        )

        if date_range:
            start_year = int(date_range.group("start_year"))
            start_month_name = date_range.group("start_month")
            start_month = cls.MONTH_MAP.get(start_month_name, 1) if start_month_name else 1
            start_date = date(start_year, start_month, 1)

            end_val = date_range.group("end_year")
            if end_val in {"present", "current"}:
                end_date = date.today()
            else:
                end_year = int(end_val)
                end_month_name = date_range.group("end_month")
                end_month = cls.MONTH_MAP.get(end_month_name, 12) if end_month_name else 12
                end_date = date(end_year, end_month, 1)

            if start_date <= end_date:
                return (start_date, end_date), 0.0

        return None, 0.0

    @staticmethod
    def _merge_intervals(intervals: List[Tuple[date, date]]) -> List[Tuple[date, date]]:
        """
        Sorts and merges overlapping date ranges into continuous blocks.
        """
        if not intervals:
            return []

        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged = [sorted_intervals[0]]

        for current_start, current_end in sorted_intervals[1:]:
            last_start, last_end = merged[-1]

            if current_start <= last_end:
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                merged.append((current_start, current_end))

        return merged

    # Professional Experience Calculation

    @classmethod
    def calculate_professional_experience(
        cls,
        experience,
    ) -> float:
        """
        Calculate total professional experience while excluding internships and
        merging overlapping full-time date ranges.
        """
        if not experience:
            return 0.0

        intervals: List[Tuple[date, date]] = []
        standalone_years = 0.0

        for item in experience:
            if cls._is_internship(item.role):
                continue

            interval, fallback_years = cls._parse_to_interval(item.duration or "")
            if interval:
                intervals.append(interval)
            else:
                standalone_years += fallback_years

        # Merge overlapping timelines
        merged = cls._merge_intervals(intervals)

        total_months = 0
        for start, end in merged:
            m = (end.year - start.year) * 12 + (end.month - start.month) + 1
            total_months += max(0, m)

        total_years = (total_months / 12) + standalone_years
        return round(total_years, 1)

    # Candidate Level Determination

    @classmethod
    def determine_level(cls, experience) -> CandidateLevel:
        """
        Determine candidate career level based on total calculated experience.

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
        years = cls.calculate_professional_experience(experience)

        if years <= 0:
            return CandidateLevel.FRESHER

        if years <= 2:
            return CandidateLevel.EARLY_CAREER

        if years <= 7:
            return CandidateLevel.EXPERIENCED

        return CandidateLevel.SENIOR