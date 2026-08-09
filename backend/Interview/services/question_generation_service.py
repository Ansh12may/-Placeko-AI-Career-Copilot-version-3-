"""
Question Generation Service

Responsible for generating ONE personalized interview
question at a time.

Responsibilities
----------------
- Build question generation prompt
- Call the LLM
- Return a validated InterviewQuestion

This service performs NO interview orchestration.
"""

from typing import List, Optional

from backend.config.settings import settings

from backend.Resume.schemas.candidate import CandidateProfile
from backend.Jobs.schemas.job import Job
from backend.Interview.schemas.interview_plan import InterviewPlan
from backend.Interview.schemas.interview_question import (
    InterviewQuestion,
    QuestionCategory,
)

from backend.Interview.prompts.question_generation_prompt import (
    QUESTION_GENERATION_PROMPT,
)

from backend.utils.llm_formatter import resume_to_llm_text
from backend.utils.text_formatter import job_to_text


class QuestionGenerationService:
    """
    Generates interview questions using the LLM.
    """

    def __init__(self):

        self.llm = settings.llm.with_structured_output(
            InterviewQuestion
        )

    def build_prompt(
        self,
        profile: CandidateProfile,
        job: Optional[Job],
        interview_plan: InterviewPlan,
        question_number: int,
        category: QuestionCategory,
        previous_questions: Optional[List[str]] = None,
    ) -> str:
        """
        Build the prompt for generating one interview question.
        """

        resume_text = resume_to_llm_text(profile)

        if job:
            job_text = job_to_text(job)
        else:
            job_text = (
                "No target job provided. "
                "Generate questions based only on the candidate's resume."
            )

        previous_questions_text = (
            "\n".join(previous_questions)
            if previous_questions
            else "None"
        )

        return QUESTION_GENERATION_PROMPT.format(

            resume=resume_text,

            job=job_text,

            interview_mode=interview_plan.interview_mode.value,

            difficulty=interview_plan.difficulty.value,

            focus_topics=", ".join(interview_plan.focus_topics),

            evaluation_criteria=", ".join(
                interview_plan.evaluation_criteria
            ),

            question_number=question_number,

            category=category.value,

            previous_questions=previous_questions_text,
        )

    def generate_question(
        self,
        profile: CandidateProfile,
        job: Optional[Job],
        interview_plan: InterviewPlan,
        question_number: int,
        category: QuestionCategory,
        previous_questions: Optional[List[str]] = None,
    ) -> InterviewQuestion:
        """
        Generate one interview question.
        """

        prompt = self.build_prompt(
            profile=profile,
            job=job,
            interview_plan=interview_plan,
            question_number=question_number,
            category=category,
            previous_questions=previous_questions,
        )

        return self.llm.invoke(prompt)