"""
Interview Flow Service

Controls the progression of an interview.

Responsibilities
----------------
- Decide the next question category
- Track interview progress
- Determine interview completion

This service performs NO LLM operations.
"""

from backend.Interview.schemas.interview_question import (
    QuestionCategory,
)

from backend.Interview.schemas.interview_session import (
    InterviewSession,
)


class InterviewFlowService:
    """
    Controls interview progression.
    """

    def _category_counts(
        self,
        session: InterviewSession,
    ) -> dict[QuestionCategory, int]:
        """
        Count how many questions have already been asked
        for each category.
        """

        counts = {
            QuestionCategory.TECHNICAL: 0,
            QuestionCategory.BEHAVIORAL: 0,
            QuestionCategory.PROJECT: 0,
        }

        for pair in session.history:

            category = pair.question.category

            if category in counts:
                counts[category] += 1

        return counts

    # ---------------------------------------------------------

    def next_category(
        self,
        session: InterviewSession,
    ) -> QuestionCategory:
        """
        Determine the category of the next question.
        """

        counts = self._category_counts(session)

        plan = session.interview_plan

        if (
            counts[QuestionCategory.TECHNICAL]
            < plan.technical_questions
        ):
            return QuestionCategory.TECHNICAL

        if (
            counts[QuestionCategory.PROJECT]
            < plan.project_questions
        ):
            return QuestionCategory.PROJECT

        if (
            counts[QuestionCategory.BEHAVIORAL]
            < plan.behavioral_questions
        ):
            return QuestionCategory.BEHAVIORAL

        # Fallback
        return QuestionCategory.TECHNICAL

    # ---------------------------------------------------------

    def total_questions(
        self,
        session: InterviewSession,
    ) -> int:
        """
        Total questions planned for the interview.
        """

        plan = session.interview_plan

        return (
            plan.technical_questions
            + plan.behavioral_questions
            + plan.project_questions
        )

    # ---------------------------------------------------------

    def remaining_questions(
        self,
        session: InterviewSession,
    ) -> int:
        """
        Number of questions remaining.
        """

        remaining = (
            self.total_questions(session)
            - len(session.history)
        )

        return max(remaining, 0)

    # ---------------------------------------------------------

    def is_interview_complete(
        self,
        session: InterviewSession,
    ) -> bool:
        """
        Determine whether the interview has finished.
        """

        return self.remaining_questions(session) == 0