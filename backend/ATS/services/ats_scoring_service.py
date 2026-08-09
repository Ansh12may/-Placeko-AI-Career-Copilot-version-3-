"""
ATS Scoring Service

Responsible for deterministic ATS scoring.

This service performs NO AI reasoning.

Responsibilities:
- Determine candidate level
- Score resume sections deterministically
- Apply candidate-level-specific weights
- Normalize section scores
- Calculate final ATS score

AI-generated qualitative feedback is handled separately
by ResumeAnalysisService.
"""

from backend.Resume.schemas.candidate import (
    CandidateProfile,
)

from backend.ATS.schemas.ats_report import (
    SectionScore,
)

from backend.ATS.schemas.candidate_level import (
    CandidateLevel,
)

from backend.ATS.services.candidate_level_service import (
    CandidateLevelService,
)


class ATSScoringService:

    # =========================================================
    # Candidate-Level Weights
    # =========================================================
    #
    # Every level totals 100 points.
    #
    # The importance of experience changes depending on
    # the candidate's career stage.
    #
    # Freshers:
    # - No professional experience penalty
    # - Projects and education matter more
    #
    # Early Career:
    # - Experience becomes more important
    #
    # Experienced:
    # - Professional experience dominates
    #
    # Senior:
    # - Professional experience is the strongest signal
    #
    # =========================================================

    WEIGHTS = {

        CandidateLevel.FRESHER: {
            "contact_information": 10,
            "education": 15,
            "projects": 25,
            "skills": 20,
            "certifications": 10,
            "formatting": 10,
            "summary": 10,
            "experience": 0,
        },

        CandidateLevel.EARLY_CAREER: {
            "contact_information": 10,
            "education": 5,
            "projects": 15,
            "skills": 20,
            "certifications": 5,
            "formatting": 10,
            "summary": 10,
            "experience": 25,
        },

        CandidateLevel.EXPERIENCED: {
            "contact_information": 10,
            "education": 5,
            "projects": 10,
            "skills": 20,
            "certifications": 5,
            "formatting": 10,
            "summary": 5,
            "experience": 35,
        },

        CandidateLevel.SENIOR: {
            "contact_information": 5,
            "education": 5,
            "projects": 10,
            "skills": 20,
            "certifications": 5,
            "formatting": 5,
            "summary": 10,
            "experience": 40,
        },
    }

    # =========================================================
    # Contact Information
    # =========================================================

    def score_contact(
        self,
        profile: CandidateProfile,
    ) -> SectionScore:

        score = 0

        if profile.name:
            score += 1

        if profile.email:
            score += 3

        if profile.phone:
            score += 2

        if profile.linkedin:
            score += 2

        if profile.github:
            score += 2

        return SectionScore(
            score=score,
            max_score=10,
        )

    # =========================================================
    # Summary
    # =========================================================

    def score_summary(
        self,
        profile: CandidateProfile,
    ) -> SectionScore:
        """
        Score the professional summary.

        The summary is evaluated for:
        - Presence
        - Reasonable length
        - Technical/career relevance

        Note:
        Candidate-level weighting is applied later.
        """

        if not profile.summary:
            return SectionScore(
                score=0,
                max_score=15,
            )

        score = 5

        words = len(
            profile.summary.split()
        )

        if words >= 25:
            score += 5

        summary_lower = (
            profile.summary.lower()
        )

        relevant_keywords = [
            "ai",
            "artificial intelligence",
            "machine learning",
            "backend",
            "software",
            "developer",
            "data science",
            "genai",
            "llm",
        ]

        if any(
            keyword in summary_lower
            for keyword in relevant_keywords
        ):
            score += 5

        return SectionScore(
            score=min(score, 15),
            max_score=15,
        )

    # =========================================================
    # Education
    # =========================================================

    def score_education(
        self,
        profile: CandidateProfile,
    ) -> SectionScore:

        score = 0

        if profile.education:

            edu = profile.education[0]

            if edu.degree:
                score += 4

            if edu.institution:
                score += 3

            if edu.year:
                score += 3

        return SectionScore(
            score=score,
            max_score=10,
        )

    # =========================================================
    # Experience
    # =========================================================

    def score_experience(
        self,
        profile: CandidateProfile,
    ) -> SectionScore:
        """
        Score professional experience.

        Experience is evaluated using:
        - Presence
        - Company
        - Role
        - Duration
        - Description quality
        """

        if not profile.experience:
            return SectionScore(
                score=0,
                max_score=20,
            )

        score = 5

        exp = profile.experience[0]

        if exp.company:
            score += 3

        if exp.role:
            score += 3

        if exp.duration:
            score += 3

        if exp.description:

            words = len(
                exp.description.split()
            )

            if words >= 20:
                score += 6
            else:
                score += 3

        return SectionScore(
            score=min(score, 20),
            max_score=20,
        )

    # =========================================================
    # Projects
    # =========================================================

    def score_projects(
        self,
        profile: CandidateProfile,
    ) -> SectionScore:
        """
        Score technical projects.

        Projects are particularly important for freshers.
        """

        if not profile.projects:
            return SectionScore(
                score=0,
                max_score=20,
            )

        score = 0

        # ---------------------------------------------
        # Number of projects
        # ---------------------------------------------

        if len(profile.projects) >= 2:
            score += 5
        else:
            score += 3

        has_description = False
        has_technologies = False
        detailed_project = False

        # ---------------------------------------------
        # Project quality
        # ---------------------------------------------

        for project in profile.projects:

            if project.description:

                has_description = True

                words = len(
                    project.description.split()
                )

                if words >= 20:
                    detailed_project = True

            if project.technologies:
                has_technologies = True

        if has_technologies:
            score += 5

        if has_description:
            score += 5

        if detailed_project:
            score += 5

        return SectionScore(
            score=min(score, 20),
            max_score=20,
        )

    # =========================================================
    # Skills
    # =========================================================

    def score_skills(
        self,
        profile: CandidateProfile,
    ) -> SectionScore:

        skills = [
            skill.lower().strip()
            for skill in profile.skills
        ]

        if not skills:
            return SectionScore(
                score=0,
                max_score=15,
            )

        score = 0

        # ---------------------------------------------
        # Skill breadth
        # ---------------------------------------------

        if len(skills) >= 5:
            score += 5

        if len(skills) >= 10:
            score += 5

        # ---------------------------------------------
        # Technical categories
        # ---------------------------------------------

        categories = {

            "languages": [
                "python",
                "java",
                "c++",
                "javascript",
                "typescript",
                "go",
                "rust",
            ],

            "frameworks": [
                "fastapi",
                "django",
                "flask",
                "react",
                "node.js",
                "express",
            ],

            "database": [
                "mongodb",
                "mysql",
                "postgresql",
                "sql",
                "redis",
            ],

            "ai": [
                "langchain",
                "langgraph",
                "machine learning",
                "deep learning",
                "llm",
                "tensorflow",
                "pytorch",
            ],
        }

        category_count = 0

        for category_skills in categories.values():

            if any(
                skill in skills
                for skill in category_skills
            ):
                category_count += 1

        if category_count >= 3:
            score += 5

        return SectionScore(
            score=min(score, 15),
            max_score=15,
        )

    # =========================================================
    # Certifications
    # =========================================================

    def score_certifications(
        self,
        profile: CandidateProfile,
    ) -> SectionScore:
        """
        Certifications are optional.

        Having certifications earns points.
        Not having them does not artificially earn
        a baseline score.
        """

        if not profile.certifications:

            return SectionScore(
                score=0,
                max_score=10,
            )

        return SectionScore(
            score=10,
            max_score=10,
        )

    # =========================================================
    # Formatting
    # =========================================================

    def score_formatting(
        self,
        profile: CandidateProfile,
    ) -> SectionScore:
        """
        Structural formatting proxy.

        The current CandidateProfile does not contain
        PDF layout information such as:
        - page count
        - font consistency
        - spacing
        - heading structure
        - hyperlink formatting

        Therefore this method evaluates whether the
        extracted resume has the expected structural
        sections.

        This is NOT a true visual formatting analysis.
        """

        score = 0

        if profile.name:
            score += 2

        if profile.education:
            score += 2

        if profile.projects:
            score += 2

        if profile.skills:
            score += 2

        if profile.certifications:
            score += 2

        return SectionScore(
            score=score,
            max_score=10,
        )

    # =========================================================
    # Normalize Score
    # =========================================================

    @staticmethod
    def _normalize_score(
        raw_score: SectionScore,
        target_max: float,
    ) -> SectionScore:
        """
        Convert a raw section score into the
        candidate-level-specific weighted score.
        """

        if target_max == 0:

            return SectionScore(
                score=0,
                max_score=0,
            )

        if raw_score.max_score == 0:

            return SectionScore(
                score=0,
                max_score=target_max,
            )

        percentage = (
            raw_score.score
            / raw_score.max_score
        )

        normalized_score = round(
            percentage * target_max,
            2,
        )

        return SectionScore(
            score=normalized_score,
            max_score=target_max,
        )

    # =========================================================
    # Calculate Final Scores
    # =========================================================

    def calculate_scores(
        self,
        profile: CandidateProfile,
    ) -> dict:
        """
        Calculate the complete deterministic ATS score.

        Pipeline:

        CandidateProfile
              ↓
        CandidateLevelService
              ↓
        Candidate Level
              ↓
        Section Scoring
              ↓
        Candidate-Level Weights
              ↓
        Normalization
              ↓
        Overall ATS Score
        """

        # -----------------------------------------------------
        # 1. Determine candidate level
        # -----------------------------------------------------

        candidate_level = (
            CandidateLevelService.determine_level(
                profile.experience
            )
        )

        # -----------------------------------------------------
        # 2. Get candidate-level weights
        # -----------------------------------------------------

        weights = self.WEIGHTS[
            candidate_level
        ]

        # -----------------------------------------------------
        # 3. Calculate raw scores
        # -----------------------------------------------------

        raw_contact = self.score_contact(
            profile
        )

        raw_summary = self.score_summary(
            profile
        )

        raw_education = self.score_education(
            profile
        )

        raw_experience = self.score_experience(
            profile
        )

        raw_projects = self.score_projects(
            profile
        )

        raw_skills = self.score_skills(
            profile
        )

        raw_certifications = (
            self.score_certifications(
                profile
            )
        )

        raw_formatting = (
            self.score_formatting(
                profile
            )
        )

        # -----------------------------------------------------
        # 4. Normalize according to candidate level
        # -----------------------------------------------------

        contact = self._normalize_score(
            raw_contact,
            weights["contact_information"],
        )

        summary = self._normalize_score(
            raw_summary,
            weights["summary"],
        )

        education = self._normalize_score(
            raw_education,
            weights["education"],
        )

        projects = self._normalize_score(
            raw_projects,
            weights["projects"],
        )

        skills = self._normalize_score(
            raw_skills,
            weights["skills"],
        )

        certifications = (
            self._normalize_score(
                raw_certifications,
                weights["certifications"],
            )
        )

        formatting = self._normalize_score(
            raw_formatting,
            weights["formatting"],
        )

        # -----------------------------------------------------
        # 5. Experience handling
        # -----------------------------------------------------

        if candidate_level == CandidateLevel.FRESHER:

            # Experience is genuinely not applicable
            # for a fresher.
            experience = SectionScore(
                score=0,
                max_score=0,
            )

        else:

            experience = self._normalize_score(
                raw_experience,
                weights["experience"],
            )

        # -----------------------------------------------------
        # 6. Calculate overall score
        # -----------------------------------------------------

        overall = round(
            contact.score
            + education.score
            + projects.score
            + skills.score
            + certifications.score
            + formatting.score
            + summary.score
            + experience.score,
            2,
        )

        # -----------------------------------------------------
        # 7. Return complete scoring result
        # -----------------------------------------------------

        return {
            "candidate_level": candidate_level,

            "overall_score": overall,

            "contact_information": contact,

            "education": education,

            "experience": experience,

            "projects": projects,

            "skills": skills,

            "certifications": certifications,

            "formatting": formatting,

            "summary": summary,
        }