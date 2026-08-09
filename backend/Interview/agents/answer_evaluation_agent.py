"""
Answer Evaluation Agent

Responsible for evaluating the candidate's latest answer
during an interview session.

Responsibilities
----------------
- Retrieve the current question-answer pair
- Invoke AnswerEvaluationService
- Store InterviewFeedback in the session

This agent contains NO business logic.
"""

from backend.Interview.schemas.interview_session import (
    InterviewSession,
)

from backend.Interview.services.answer_evaluation_service import (
    AnswerEvaluationService,
)


class AnswerEvaluationAgent:
    """
    Orchestrates interview answer evaluation.
    """

    def __init__(self):
        self.service = AnswerEvaluationService()

    # ---------------------------------------------------------

    def run(
        self,
        session: InterviewSession,
    ) -> InterviewSession:
        """
        Evaluate the current interview answer.
        """

        if not session.history:
            raise ValueError(
                "Interview session contains no questions."
            )

        pair = session.history[
            session.current_question_index
        ]

        if pair.answer is None:
            raise ValueError(
                "Cannot evaluate because no answer has been submitted."
            )

        feedback = self.service.evaluate(
            profile=session.candidate,
            job=session.target_job,
            question=pair.question,
            answer=pair.answer,
        )

        if feedback is None:
            raise ValueError(
                "Failed to generate interview feedback."
            )

        pair.feedback = feedback

        pair.interaction_completed = True

        return session