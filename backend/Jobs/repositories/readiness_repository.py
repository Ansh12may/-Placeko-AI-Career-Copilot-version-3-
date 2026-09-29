"""
Repository for human verification decisions used by the
Job Readiness & Gap Evidence Engine.
"""

from datetime import datetime, timezone
from typing import List

from backend.database.db import database


class ReadinessRepository:
    COLLECTION_NAME = "job_readiness_confirmations"

    def _get_collection(self):
        if database.db is None:
            raise RuntimeError("Database is not connected.")
        return database.db[self.COLLECTION_NAME]

    async def get_confirmations(
        self,
        user_id: str,
        resume_id: str,
        job_key: str,
    ) -> List[str]:
        document = await self._get_collection().find_one(
            {
                "user_id": user_id,
                "resume_id": resume_id,
                "job_key": job_key,
            }
        )
        if not document:
            return []
        return document.get("requirements", [])

    async def confirm_requirement(
        self,
        user_id: str,
        resume_id: str,
        job_key: str,
        requirement: str,
    ) -> None:
        collection = self._get_collection()
        await collection.update_one(
            {
                "user_id": user_id,
                "resume_id": resume_id,
                "job_key": job_key,
            },
            {
                "$addToSet": {"requirements": requirement},
                "$set": {"updated_at": datetime.now(timezone.utc)},
                "$setOnInsert": {"created_at": datetime.now(timezone.utc)},
            },
            upsert=True,
        )
