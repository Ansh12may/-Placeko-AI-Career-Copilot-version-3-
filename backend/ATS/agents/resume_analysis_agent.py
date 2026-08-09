"""
Resume Analysis Agent

Responsible for generating a complete ATS report.

Responsibilities:
- Read CandidateProfile from GraphState
- Calculate deterministic ATS scores
- Invoke ResumeAnalysisService for qualitative feedback
- Merge deterministic scores with AI feedback
- Create ATSReport
- Update GraphState

This agent performs orchestration only.

It does NOT:
- Parse resumes
- Perform MongoDB operations
- Search for jobs
- Perform job ranking
"""

from backend.graphs.state import GraphState
from backend.Resume.schemas.candidate import CandidateProfile
from backend.ATS.schemas.ats_report import ATSReport

from backend.ATS.services.resume_analysis_service import (
    ResumeAnalysisService,
)

from backend.ATS.services.ats_scoring_service import (
    ATSScoringService,
)


class ResumeAnalysisAgent:

    def __init__(self):
        self.analysis_service = (
            ResumeAnalysisService()
        )

        self.ats_scoring_service = (
            ATSScoringService()
        )

    # =========================================================
    # Prepare Input
    # =========================================================

    def prepare_input(
        self,
        state: GraphState,
    ) -> CandidateProfile:
        """
        Extract CandidateProfile from GraphState.
        """

        profile = state.get(
            "candidate_profile"
        )

        if profile is None:
            raise ValueError(
                "Candidate profile not found in GraphState."
            )

        return profile

    # =========================================================
    # Build ATS Report
    # =========================================================

    def build_report(
        self,
        scores: dict,
        analysis: dict,
    ) -> ATSReport:
        """
        Merge deterministic ATS scores with
        AI-generated qualitative feedback.
        """

        return ATSReport(
            # -------------------------------------------------
            # Candidate Level
            # -------------------------------------------------

            candidate_level=scores[
                "candidate_level"
            ],

            # -------------------------------------------------
            # Overall Score
            # -------------------------------------------------

            overall_score=scores[
                "overall_score"
            ],

            # -------------------------------------------------
            # Section Scores
            # -------------------------------------------------

            contact_information=scores[
                "contact_information"
            ],

            education=scores[
                "education"
            ],

            experience=scores[
                "experience"
            ],

            projects=scores[
                "projects"
            ],

            skills=scores[
                "skills"
            ],

            certifications=scores[
                "certifications"
            ],

            formatting=scores[
                "formatting"
            ],

            summary=scores[
                "summary"
            ],

            # -------------------------------------------------
            # AI Qualitative Analysis
            # -------------------------------------------------

            strengths=analysis.get(
                "strengths",
                [],
            ),

            weaknesses=analysis.get(
                "weaknesses",
                [],
            ),

            missing_keywords=analysis.get(
                "missing_keywords",
                [],
            ),

            # -------------------------------------------------
            # Section Feedback
            # -------------------------------------------------

            formatting_feedback=analysis.get(
                "formatting_feedback",
                [],
            ),

            education_feedback=analysis.get(
                "education_feedback",
                [],
            ),

            experience_feedback=analysis.get(
                "experience_feedback",
                [],
            ),

            project_feedback=analysis.get(
                "project_feedback",
                [],
            ),

            skills_feedback=analysis.get(
                "skills_feedback",
                [],
            ),

            # -------------------------------------------------
            # Recommendations
            # -------------------------------------------------

            recommendations=analysis.get(
                "recommendations",
                [],
            ),
        )

    # =========================================================
    # Run
    # =========================================================

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute the ATS analysis pipeline.

        Flow:

        GraphState
            ↓
        CandidateProfile
            ↓
        ATSScoringService
            ↓
        ResumeAnalysisService
            ↓
        ATSReport
            ↓
        GraphState
        """

        # -----------------------------------------------------
        # 1. Get candidate profile
        # -----------------------------------------------------

        profile = self.prepare_input(
            state
        )

        # -----------------------------------------------------
        # 2. Calculate deterministic scores
        # -----------------------------------------------------

        scores = (
            self.ats_scoring_service
            .calculate_scores(
                profile
            )
        )

        # -----------------------------------------------------
        # 3. Generate qualitative AI feedback
        # -----------------------------------------------------

        analysis = (
            self.analysis_service
            .analyze_resume(
                profile
            )
        )

        # -----------------------------------------------------
        # 4. Build final ATS report
        # -----------------------------------------------------

        report = self.build_report(
            scores=scores,
            analysis=analysis,
        )

        # -----------------------------------------------------
        # 5. Store report in GraphState
        # -----------------------------------------------------

        state["ats_report"] = report

        return state