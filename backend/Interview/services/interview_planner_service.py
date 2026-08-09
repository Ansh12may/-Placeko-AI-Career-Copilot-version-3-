"""
Interview Planner Service

Responsible for generating a personalized interview
plan using the candidate profile, target job,
and interview configuration.

Responsibilities:
- Prepare planner prompt
- Call the LLM
- Return a validated InterviewPlan

This service performs NO interview orchestration.
"""

from backend.config.settings import settings

from backend.Resume.schemas.candidate import CandidateProfile
from backend.Jobs.schemas.job import Job

from backend.Interview.schemas.interview_plan import (
    InterviewPlan,
    InterviewMode,
    DifficultyLevel,
)

from backend.Interview.prompts.interview_planner_prompt import (
    INTERVIEW_PLANNER_PROMPT,
)

from backend.utils.llm_formatter import resume_to_llm_text
from backend.utils.text_formatter import job_to_text


class InterviewPlannerService:
    """
    Generates a structured InterviewPlan using the LLM.
    """

    def __init__(self):
        self.llm = settings.llm.with_structured_output(
            InterviewPlan
        )

    def build_prompt(
        self,
        profile: CandidateProfile,
        job: Job,
        interview_mode: InterviewMode,
        difficulty: DifficultyLevel,
    ) -> str:
        """
        Build the interview planner prompt.
        """

        resume_text = resume_to_llm_text(profile)
        job_text = (
        job_to_text(job)
        if job
        else "No target job provided. Generate a general interview plan based on the candidate's resume."
        )

        return INTERVIEW_PLANNER_PROMPT.format(
            resume=resume_text,
            job=job_text,
            interview_mode=interview_mode.value,
            difficulty=difficulty.value,
        )

    def generate_plan(
    self,
    profile: CandidateProfile,
    interview_mode: InterviewMode,
    difficulty: DifficultyLevel,
    job: Job | None = None,
) -> InterviewPlan:
        """
        Generate a personalized interview plan.
        """

        prompt = self.build_prompt(
            profile=profile,
            job=job,
            interview_mode=interview_mode,
            difficulty=difficulty,
        )

        interview_plan = self.llm.invoke(prompt)
        if interview_plan is None:
            raise ValueError("Failed to generate interview plan.")

        return interview_plan