"""
Resume Analysis Service

Responsible for:
- Preparing structured candidate data for the LLM
- Determining candidate career level
- Invoking the LLM for qualitative resume analysis
- Returning structured qualitative feedback

This service does NOT calculate ATS scores.

Deterministic numerical scoring is handled by:
    ATSScoringService
"""

from pydantic import BaseModel, Field
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from backend.config.settings import settings

from backend.Resume.schemas.candidate import (
    CandidateProfile,
)

from backend.ATS.prompts.resume_analysis_prompt import (
    RESUME_ANALYSIS_PROMPT,
)

from backend.ATS.services.candidate_level_service import (
    CandidateLevelService,
)

from backend.utils.llm_formatter import (
    resume_to_llm_text,
)


# =========================================================
# Structured LLM Output
# =========================================================

class ResumeQualitativeAnalysis(BaseModel):
    """
    Structured qualitative analysis produced by the LLM.

    The LLM does NOT calculate numerical ATS scores.
    """

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    missing_keywords: list[str] = Field(
        default_factory=list
    )

    formatting_feedback: list[str] = Field(
        default_factory=list
    )

    education_feedback: list[str] = Field(
        default_factory=list
    )

    experience_feedback: list[str] = Field(
        default_factory=list
    )

    project_feedback: list[str] = Field(
        default_factory=list
    )

    skills_feedback: list[str] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
        default_factory=list
    )


# =========================================================
# Resume Analysis Service
# =========================================================

class ResumeAnalysisService:

    def __init__(self):
        self.llm = settings.llm

    # =====================================================
    # Candidate Level
    # =====================================================

    def determine_candidate_level(
        self,
        profile: CandidateProfile,
    ):
        """
        Determine the candidate's career level.

        Uses the same CandidateLevelService as
        ATSScoringService so both numerical scoring
        and qualitative analysis use the same classification.
        """

        return (
            CandidateLevelService.determine_level(
                profile.experience
            )
        )

    # =====================================================
    # Build Prompt
    # =====================================================

    def build_prompt(
        self,
        profile: CandidateProfile,
    ) -> str:
        """
        Build the qualitative resume analysis prompt.

        Candidate level is explicitly passed to the LLM
        so that feedback is appropriate for the candidate's
        career stage.
        """

        candidate_level = (
            self.determine_candidate_level(
                profile
            )
        )

        resume_text = resume_to_llm_text(
            profile
        )

        return RESUME_ANALYSIS_PROMPT.format(
            candidate_level=(
                candidate_level.value
            ),
            resume=resume_text,
        )

    # =====================================================
    # Analyze Resume
    # =====================================================

    def analyze_resume(
        self,
        profile: CandidateProfile,
    ) -> dict:
        """
        Generate qualitative resume feedback.

        This method does NOT calculate:
        - ATS scores
        - Section scores
        - Percentages
        - Numerical ratings
        """

        prompt = self.build_prompt(
            profile
        )

        messages = [
            SystemMessage(
                 content=(

        "You are an evidence-based Technical Recruiter "
        "and ATS Resume Reviewer. Analyze ONLY information "
        "contained in the supplied resume. Ground every "
        "important claim in resume evidence. Never invent "
        "skills, achievements, experience, technologies, "
        "metrics, or certifications. Follow the candidate "
        "career level provided in the prompt. Return only "
        "the JSON structure requested by the user prompt."

    )
            ),
            HumanMessage(
                content=prompt
            ),
        ]

        # -------------------------------------------------
        # Structured LLM output
        # -------------------------------------------------

        structured_llm = (
            self.llm.with_structured_output(
                ResumeQualitativeAnalysis,
                method="json_mode",
            )
        )

        result = structured_llm.invoke(
            messages
        )

        # -------------------------------------------------
        # Pydantic result
        # -------------------------------------------------

        if isinstance(
            result,
            ResumeQualitativeAnalysis,
        ):
            return result.model_dump()

        # -------------------------------------------------
        # Dictionary result
        # -------------------------------------------------

        if isinstance(
            result,
            dict,
        ):
            return result

        # -------------------------------------------------
        # Generic Pydantic-compatible result
        # -------------------------------------------------

        if hasattr(
            result,
            "model_dump",
        ):
            return result.model_dump()

        # -------------------------------------------------
        # Defensive fallback
        # -------------------------------------------------

        return {
            "strengths": [],
            "weaknesses": [],
            "missing_keywords": [],
            "formatting_feedback": [],
            "education_feedback": [],
            "experience_feedback": [],
            "project_feedback": [],
            "skills_feedback": [],
            "recommendations": [],
        }