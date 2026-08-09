"""
Interview Session Agent

Maintains the InterviewSession state.

Responsibilities
----------------
- Start an interview session
- Add generated questions
- Store candidate answers
- Store evaluation feedback
- Advance interview progress
- Complete the interview session

This agent performs NO LLM operations and contains NO
business logic.
"""

from datetime import datetime

from backend.Interview.schemas.interview_session import (
    InterviewSession,
    InterviewStatus,
)

from backend.Interview.schemas.question_answer_pair import (
    QuestionAnswerPair,
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

from backend.Interview.schemas.interview_report import (
    InterviewReport,
)


class InterviewSessionAgent:
    """
    Maintains InterviewSession throughout the interview lifecycle.
    """

    # ---------------------------------------------------------
    # Start Interview
    # ---------------------------------------------------------

    def start_interview(
        self,
        session: InterviewSession,
    ) -> InterviewSession:
        """
        Mark interview as started.
        """

        session.status = InterviewStatus.IN_PROGRESS
        session.started_at = datetime.utcnow()

        return session

    # ---------------------------------------------------------
    # Add Question
    # ---------------------------------------------------------

    def add_question(
        self,
        session: InterviewSession,
        question: InterviewQuestion,
    ) -> InterviewSession:
        """
        Add a newly generated interview question.
        """

        session.history.append(
            QuestionAnswerPair(
                question=question
            )
        )

        session.current_question_index = (
            len(session.history) - 1
        )

        return session

    # ---------------------------------------------------------
    # Add Answer
    # ---------------------------------------------------------

    def add_answer(
        self,
        session: InterviewSession,
        answer: InterviewAnswer,
    ) -> InterviewSession:
        """
        Store candidate answer.
        """

        if not session.history:
            raise ValueError(
                "No interview question exists."
            )

        session.history[
            session.current_question_index
        ].answer = answer

        return session

    # ---------------------------------------------------------
    # Add Feedback
    # ---------------------------------------------------------

    def add_feedback(
        self,
        session: InterviewSession,
        feedback: InterviewFeedback,
    ) -> InterviewSession:
        """
        Store AI evaluation.
        """

        if not session.history:
            raise ValueError(
                "No interview question exists."
            )

        pair = session.history[
            session.current_question_index
        ]

        pair.feedback = feedback
        pair.interaction_completed = True

        return session

    # ---------------------------------------------------------
    # Advance Question
    # ---------------------------------------------------------

    def advance_question(
        self,
        session: InterviewSession,
    ) -> InterviewSession:
        """
        Move to the next interview question.
        """

        session.current_question_index += 1

        return session

    # ---------------------------------------------------------
    # Attach Report
    # ---------------------------------------------------------

    def attach_report(
        self,
        session: InterviewSession,
        report: InterviewReport,
    ) -> InterviewSession:
        """
        Attach the generated interview report.
        """

        session.report = report

        return session

    # ---------------------------------------------------------
    # Finish Interview
    # ---------------------------------------------------------

    def finish_interview(
        self,
        session: InterviewSession,
    ) -> InterviewSession:
        """
        Mark interview as completed.
        """

        session.status = InterviewStatus.COMPLETED
        session.ended_at = datetime.utcnow()
        session.current_question_index = -1

        return session