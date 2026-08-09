"""
Answer Evaluation Service

Evaluates a candidate's answer using the LLM.

Responsibilities
----------------
- Build evaluation prompt
- Invoke the LLM
- Return a validated InterviewFeedback

This service performs NO interview orchestration.
"""

from typing import Optional

from backend.config.settings import settings

from backend.Resume.schemas.candidate import CandidateProfile
from backend.Jobs.schemas.job import Job

from backend.utils.llm_formatter import resume_to_llm_text
from backend.utils.text_formatter import job_to_text

from backend.Interview.prompts.answer_evaluation_prompt import (
    ANSWER_EVALUATION_PROMPT,
)

from backend.Interview.schemas.interview_question import (
    InterviewQuestion,
)

from backend.Interview.schemas.interview_answer import (
    InterviewAnswer,
)

from backend.Interview.schemas.interview_feedback import (
    InterviewFeedback,
)


class AnswerEvaluationService:
    """
    Service responsible for evaluating one interview answer.
    """

    def __init__(self):
       self.llm = settings.llm.with_structured_output(
            InterviewFeedback
        )

    def build_prompt(
        self,
        profile: CandidateProfile,
        job: Optional[Job],
        question: InterviewQuestion,
        answer: InterviewAnswer,
    ) -> str:
        """
        Build the evaluation prompt.
        """

        resume_text = resume_to_llm_text(profile)

        job_text = (
            job_to_text(job)
            if job
            else "No target job provided."
        )

        return ANSWER_EVALUATION_PROMPT.format(
            resume=resume_text,
            job=job_text,
            question=question.question,
            category=question.category.value,
            difficulty=question.difficulty.value,
            focus_topic=question.focus_topic,
            expected_topics="\n".join(question.expected_topics),
            answer=answer.transcript,
        )

    def evaluate(
        self,
        profile: CandidateProfile,
        job: Optional[Job],
        question: InterviewQuestion,
        answer: InterviewAnswer,
    ) -> InterviewFeedback:
        """
        Evaluate one interview answer.
        """

        prompt = self.build_prompt(
            profile=profile,
            job=job,
            question=question,
            answer=answer,
        )

        feedback = self.llm.invoke(prompt)

        if feedback is None:
            raise ValueError(
                "Failed to generate interview feedback."
            )

        return feedback