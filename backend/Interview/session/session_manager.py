"""
Interview Session Manager

Responsible for:
- Creating interview sessions
- Retrieving interview sessions
- Updating interview sessions
- Deleting interview sessions

Persistence is delegated to InterviewRepository.

This class contains NO business logic.
"""

from backend.Interview.schemas.interview_session import (
    InterviewSession,
)

from backend.Interview.repositories.interview_repository import (
    InterviewRepository,
)


class InterviewSessionManager:
    """
    Manages persistent interview sessions.
    """

    def __init__(self):
        self.repository = InterviewRepository()

    # =========================================================
    # CREATE
    # =========================================================

    async def create_session(
        self,
        session: InterviewSession,
    ) -> InterviewSession:
        """
        Persist a new interview session.
        """

        interview_data = session.model_dump(
            mode="json"
        )

        await self.repository.create_interview(
            interview_data
        )

        return session

    # =========================================================
    # GET
    # =========================================================

    async def get_session(
        self,
        session_id: str,
        user_id: str,
    ) -> InterviewSession:
        """
        Retrieve an interview session belonging
        to the authenticated user.
        """

        interview = (
            await self.repository.get_by_session_id(
                session_id=session_id,
                user_id=user_id,
            )
        )

        if interview is None:
            raise ValueError(
                f"Interview session '{session_id}' not found."
            )

        return InterviewSession.model_validate(
            interview
        )

    # =========================================================
    # UPDATE
    # =========================================================

    async def update_session(
        self,
        session: InterviewSession,
    ) -> InterviewSession:
        """
        Persist changes to an interview session.
        """

        interview_data = session.model_dump(
            mode="json"
        )

        await self.repository.update_by_session_id(
            session_id=session.session_id,
            user_id=session.user_id,
            interview_data=interview_data,
        )

        return session

    # =========================================================
    # DELETE
    # =========================================================

    async def delete_session(
        self,
        session_id: str,
        user_id: str,
    ) -> None:
        """
        Delete an interview session.
        """

        await self.repository.delete_by_session_id(
            session_id=session_id,
            user_id=user_id,
        )

    # =========================================================
    # LIST USER INTERVIEWS
    # =========================================================

    async def list_sessions(
        self,
        user_id: str,
    ) -> list[InterviewSession]:
        """
        Retrieve all interview sessions belonging
        to the authenticated user.
        """

        interviews = (
            await self.repository.get_user_interviews(
                user_id=user_id,
            )
        )

        return [
            InterviewSession.model_validate(
                interview
            )
            for interview in interviews
        ]

    # =========================================================
    # LIST COMPLETED INTERVIEWS
    # =========================================================

    async def list_completed_sessions(
        self,
        user_id: str,
    ) -> list[InterviewSession]:
        """
        Retrieve completed interview sessions.
        """

        interviews = (
            await self.repository.get_completed_interviews(
                user_id=user_id,
            )
        )

        return [
            InterviewSession.model_validate(
                interview
            )
            for interview in interviews
        ]