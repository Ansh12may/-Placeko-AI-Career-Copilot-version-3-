"""
Job Recommendation Repository

Responsible for:
- Persisting personalized job recommendations.
- Retrieving recommendations for a user and resume.

This repository performs NO:
- Job searching
- LLM reasoning
- Vector retrieval
- Ranking
- Recommendation business logic
"""

from datetime import datetime, timezone
from typing import List, Optional

from backend.database.db import database
from backend.Jobs.schemas.job import Job


class JobRepository:
    """
    MongoDB repository for persisted job recommendations.
    """

    COLLECTION_NAME = "job_recommendations"

    def _get_collection(self):
        """
        Return the MongoDB job recommendations collection.
        """

        if database.db is None:
            raise RuntimeError(
                "Database is not connected."
            )

        return database.db[
            self.COLLECTION_NAME
        ]

    # =========================================================
    # GET RECOMMENDATIONS
    # =========================================================

    async def get_recommendations(
        self,
        user_id: str,
        resume_id: str,
    ) -> Optional[List[Job]]:
        """
        Retrieve persisted recommendations belonging
        to the authenticated user and resume.
        """

        collection = self._get_collection()

        document = await collection.find_one(
            {
                "user_id": user_id,
                "resume_id": resume_id,
            }
        )

        if not document:
            return None

        return [
            Job.model_validate(job)
            for job in document.get(
                "jobs",
                [],
            )
        ]
    # =========================================================
    # GET SINGLE JOB
    # =========================================================

    async def get_job(
        self,
        user_id: str,
        resume_id: str,
        job_id: str,
    ) -> Optional[Job]:
        """
        Retrieve a single persisted recommendation
        belonging to the authenticated user and resume.
        """

        collection = self._get_collection()

        document = await collection.find_one(
            {
                "user_id": user_id,
                "resume_id": resume_id,
                "jobs.job_id": job_id,
            }
        )

        if not document:
            return None

        for job in document.get("jobs", []):
            if job.get("job_id") == job_id:
                return Job.model_validate(job)

        return None

    # =========================================================
    # SAVE RECOMMENDATIONS
    # =========================================================

    async def save_recommendations(
        self,
        user_id: str,
        resume_id: str,
        jobs: List[Job],
    ) -> None:
        """
        Persist the latest recommendation snapshot
        for a user and resume.
        """

        collection = self._get_collection()

        document = {
            "user_id": user_id,
            "resume_id": resume_id,
            "jobs": [
                job.model_dump(
                    mode="json"
                )
                for job in jobs
            ],
            "generated_at": datetime.now(
                timezone.utc
            ),
        }

        await collection.update_one(
            {
                "user_id": user_id,
                "resume_id": resume_id,
            },
            {
                "$set": document,
            },
            upsert=True,
        )