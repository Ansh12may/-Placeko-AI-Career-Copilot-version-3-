"""
Resume Repository

Responsible for:
- Resume CRUD operations
- MongoDB interactions

This repository performs NO business logic.
"""

from bson import ObjectId
from backend.database.db import database


class ResumeRepository:

    @property
    def collection(self):
        return database.db["resumes"]

    # =========================================================
    # Serialization Helpers
    # =========================================================

    @staticmethod
    def _serialize_resume(resume: dict | None):

        if resume is None:
            return None

        if "_id" in resume:
            resume["id"] = str(resume.pop("_id"))

        return resume

    @classmethod
    def _serialize_resumes(
        cls,
        resumes: list[dict],
    ):
        return [
            cls._serialize_resume(resume)
            for resume in resumes
        ]

    # =========================================================
    # Create
    # =========================================================

    async def create_resume(
        self,
        resume_data: dict,
    ) -> str:

        result = await self.collection.insert_one(
            resume_data
        )

        return str(result.inserted_id)

    # =========================================================
    # Get All User Resumes
    # =========================================================

    async def get_user_resumes(
        self,
        user_id: str,
    ):

        cursor = (
            self.collection
            .find(
                {
                    "user_id": user_id,
                }
            )
            .sort(
                "created_at",
                -1,
            )
        )

        resumes = await cursor.to_list(
            length=None
        )

        return self._serialize_resumes(
            resumes
        )

    # =========================================================
    # Get Resume By ID
    # =========================================================

    async def get_resume_by_id(
        self,
        resume_id: str,
        user_id: str,
    ):

        resume = await self.collection.find_one(
            {
                "_id": ObjectId(resume_id),
                "user_id": user_id,
            }
        )

        return self._serialize_resume(
            resume
        )

    # =========================================================
    # Get Active Resume
    # =========================================================

    async def get_active_resume(
        self,
        user_id: str,
    ):

        resume = await self.collection.find_one(
            {
                "user_id": user_id,
                "is_active": True,
            }
        )

        return self._serialize_resume(
            resume
        )

    # =========================================================
    # Update Resume
    # =========================================================

    async def update_resume(
        self,
        resume_id: str,
        user_id: str,
        update_data: dict,
    ):

        return await self.collection.update_one(
            {
                "_id": ObjectId(resume_id),
                "user_id": user_id,
            },
            {
                "$set": update_data,
            },
        )

    # =========================================================
    # Delete Resume
    # =========================================================

    async def delete_resume(
        self,
        resume_id: str,
        user_id: str,
    ):

        return await self.collection.delete_one(
            {
                "_id": ObjectId(resume_id),
                "user_id": user_id,
            }
        )

    # =========================================================
    # Deactivate All Resumes
    # =========================================================

    async def deactivate_all_resumes(
        self,
        user_id: str,
    ):

        await self.collection.update_many(
            {
                "user_id": user_id,
            },
            {
                "$set": {
                    "is_active": False,
                }
            },
        )