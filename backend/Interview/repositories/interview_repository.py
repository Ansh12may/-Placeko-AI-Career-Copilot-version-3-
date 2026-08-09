"""
Interview Repository

Responsible for:
- Interview session persistence
- MongoDB interactions
- Fetching interview history for users

This repository performs NO business logic.
"""

from bson import ObjectId

from backend.database.db import database


class InterviewRepository:

    @property
    def collection(self):
        return database.db["interviews"]

    # =========================================================
    # Serialization
    # =========================================================

    @staticmethod
    def _serialize_interview(
        interview: dict | None,
    ):
        """
        Convert MongoDB document into a JSON-compatible
        dictionary.
        """

        if interview is None:
            return None

        if "_id" in interview:
            interview["id"] = str(
                interview.pop("_id")
            )

        return interview

    # =========================================================
    # Create
    # =========================================================

    async def create_interview(
        self,
        interview_data: dict,
    ) -> str:
        """
        Store a new interview session.
        """

        result = await self.collection.insert_one(
            interview_data
        )

        return str(
            result.inserted_id
        )

    # =========================================================
    # Get By Session ID
    # =========================================================

    async def get_by_session_id(
        self,
        session_id: str,
        user_id: str,
    ):
        """
        Retrieve an interview belonging to
        the authenticated user.
        """

        interview = await self.collection.find_one(
            {
                "session_id": session_id,
                "user_id": user_id,
            }
        )

        return self._serialize_interview(
            interview
        )

    # =========================================================
    # Update
    # =========================================================

    async def update_by_session_id(
        self,
        session_id: str,
        user_id: str,
        interview_data: dict,
    ):
        """
        Update an existing interview session.
        """

        return await self.collection.update_one(
            {
                "session_id": session_id,
                "user_id": user_id,
            },
            {
                "$set": interview_data,
            },
        )

    # =========================================================
    # Delete
    # =========================================================

    async def delete_by_session_id(
        self,
        session_id: str,
        user_id: str,
    ):
        """
        Delete an interview session belonging
        to the authenticated user.
        """

        return await self.collection.delete_one(
            {
                "session_id": session_id,
                "user_id": user_id,
            }
        )

    # =========================================================
    # Get User Interviews
    # =========================================================

    async def get_user_interviews(
        self,
        user_id: str,
    ):
        """
        Retrieve all interviews belonging to
        the authenticated user.

        Newest interviews are returned first.
        """

        cursor = (
            self.collection
            .find(
                {
                    "user_id": user_id,
                }
            )
            .sort(
                "started_at",
                -1,
            )
        )

        interviews = await cursor.to_list(
            length=None
        )

        return [
            self._serialize_interview(
                interview
            )
            for interview in interviews
        ]

    # =========================================================
    # Get User Completed Interviews
    # =========================================================

    async def get_completed_interviews(
        self,
        user_id: str,
    ):
        """
        Retrieve completed interviews for the
        authenticated user.
        """

        cursor = (
            self.collection
            .find(
                {
                    "user_id": user_id,
                    "status": "Completed",
                }
            )
            .sort(
                "ended_at",
                -1,
            )
        )

        interviews = await cursor.to_list(
            length=None
        )

        return [
            self._serialize_interview(
                interview
            )
            for interview in interviews
        ]