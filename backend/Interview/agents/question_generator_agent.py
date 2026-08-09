"""
Question Generator Agent

Responsible for orchestrating interview question generation.

Responsibilities
----------------
- Read required inputs from GraphState
- Invoke QuestionGenerationService
- Store generated question in GraphState

This agent contains NO business logic.
"""

from typing import Optional

from backend.graphs.state import GraphState

from backend.Resume.schemas.candidate import CandidateProfile
from backend.Jobs.schemas.job import Job

from backend.Interview.schemas.interview_plan import (
    InterviewPlan,
)

from backend.Interview.schemas.interview_question import (
    InterviewQuestion,
    QuestionCategory,
)

from backend.Interview.services.question_generation_service import (
    QuestionGenerationService,
)


class QuestionGeneratorAgent:
    """
    Orchestrates interview question generation.
    """

    def __init__(self):
        self.question_service = QuestionGenerationService()

    # ---------------------------------------------------------

    def prepare_input(
        self,
        state: GraphState,
    ) -> tuple[
        CandidateProfile,
        Optional[Job],
        InterviewPlan,
        int,
        QuestionCategory,
        list[str],
    ]:
        """
        Extract required inputs from GraphState.
        """

        profile = state.get("candidate_profile")

        job = state.get("selected_job")

        interview_plan = state.get("interview_plan")

        question_number = state.get(
            "question_number",
            1,
        )

        category = state.get(
            "current_category",
            QuestionCategory.TECHNICAL,
        )

        previous_questions = state.get(
            "previous_questions",
            [],
        )

        if profile is None:
            raise ValueError(
                "Candidate profile missing."
            )

        if interview_plan is None:
            raise ValueError(
                "Interview plan missing."
            )

        return (
            profile,
            job,
            interview_plan,
            question_number,
            category,
            previous_questions,
        )

    # ---------------------------------------------------------

    def invoke_service(
        self,
        profile: CandidateProfile,
        job: Optional[Job],
        interview_plan: InterviewPlan,
        question_number: int,
        category: QuestionCategory,
        previous_questions: list[str],
    ) -> InterviewQuestion:
        """
        Invoke the Question Generation Service.
        """

        return self.question_service.generate_question(
            profile=profile,
            job=job,
            interview_plan=interview_plan,
            question_number=question_number,
            category=category,
            previous_questions=previous_questions,
        )

    # ---------------------------------------------------------

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Generate one interview question and update GraphState.
        """

        inputs = self.prepare_input(state)

        interview_question = self.invoke_service(*inputs)

        if interview_question is None:
            raise ValueError(
                "Failed to generate interview question."
            )

        state["current_question"] = interview_question

        state["current_question_id"] = (
            interview_question.question_id
        )

        previous_questions = state.get(
            "previous_questions",
            [],
        )

        previous_questions.append(
            interview_question.question
        )

        state["previous_questions"] = previous_questions

        current_number = state.get(
            "question_number",
            1,
        )

        state["question_number"] = (
            current_number + 1
        )

        return state