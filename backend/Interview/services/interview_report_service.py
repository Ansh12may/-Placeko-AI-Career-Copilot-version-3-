"""
Interview Report Service

Generates the final interview report after the
interview has been completed.

Responsibilities
----------------
- Convert interview history into LLM-friendly text
- Build the report prompt
- Invoke the LLM
- Return a validated InterviewReport

This service performs NO interview orchestration.
"""

from backend.config.settings import settings

from backend.Resume.schemas.candidate import CandidateProfile
from backend.Jobs.schemas.job import Job

from backend.utils.llm_formatter import resume_to_llm_text
from backend.utils.text_formatter import job_to_text

from backend.Interview.prompts.interview_report_prompt import (
    INTERVIEW_REPORT_PROMPT,
)

from backend.Interview.schemas.interview_session import (
    InterviewSession,
)

from backend.Interview.schemas.interview_report import (
    InterviewReport,
)


class InterviewReportService:
    """
    Generates the final interview report.
    """

    def __init__(self):
        self.llm = settings.llm.with_structured_output(
            InterviewReport
        )

    # ---------------------------------------------------------

    def history_to_text(
        self,
        session: InterviewSession,
    ) -> str:
        """
        Convert the interview history into an LLM-friendly format.
        """

        history = []

        for index, pair in enumerate(session.history, start=1):

            strengths = (
                "\n".join(pair.feedback.strengths)
                if pair.feedback
                else ""
            )

            weaknesses = (
                "\n".join(pair.feedback.weaknesses)
                if pair.feedback
                else ""
            )

            missing_topics = (
                "\n".join(pair.feedback.missing_topics)
                if pair.feedback
                else ""
            )

            suggestions = (
                "\n".join(pair.feedback.suggestions)
                if pair.feedback
                else ""
            )

            overall_score = (
                pair.feedback.overall.score
                if pair.feedback
                else "N/A"
            )

            answer = (
                pair.answer.transcript
                if pair.answer
                else "Not Answered"
            )

            history.append(
                f"""
Question {index}
----------------
Category:
{pair.question.category.value}

Difficulty:
{pair.question.difficulty.value}

Question:
{pair.question.question}

Candidate Answer:
{answer}

Evaluation

Overall Score:
{overall_score}

Strengths:
{strengths}

Weaknesses:
{weaknesses}

Missing Topics:
{missing_topics}

Suggestions:
{suggestions}
"""
            )

        return "\n\n".join(history)

    

    def build_prompt(
        self,
        session: InterviewSession,
    ) -> str:
        """
        Build the report generation prompt.
        """

        resume_text = resume_to_llm_text(
            session.candidate
        )

        job_text = (
            job_to_text(session.target_job)
            if session.target_job
            else "No target job provided."
        )

        interview_history = self.history_to_text(
            session
        )

        return INTERVIEW_REPORT_PROMPT.format(
            resume=resume_text,
            job=job_text,
            interview_plan=session.interview_plan.model_dump_json(
                indent=2
            ),
            interview_history=interview_history,
        )

    

    def generate_report(
        self,
        session: InterviewSession,
    ) -> InterviewReport:
        """
        Generate the final interview report.
        """

        prompt = self.build_prompt(session)

        report = self.llm.invoke(prompt)

        if report is None:
            raise ValueError(
                "Failed to generate interview report."
            )

        return report