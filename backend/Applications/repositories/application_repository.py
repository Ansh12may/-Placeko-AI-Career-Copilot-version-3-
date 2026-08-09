"""
Application Repository

Responsible for storing and retrieving application records
from MongoDB.

This repository contains database-specific logic only.
It does NOT contain application business logic.
"""

from typing import List, Optional

from backend.Applications.schemas.application import (
    Application,
)

from backend.database.db import database


class ApplicationRepository:
    """
    MongoDB repository for application tracking data.
    """

    COLLECTION_NAME = "applications"

    def __init__(self):
        self.collection = None

    # =========================================================
    # COLLECTION
    # =========================================================

    def _get_collection(self):
        """
        Return the MongoDB applications collection.
        """

        if database.db is None:
            raise RuntimeError(
                "Database is not connected."
            )

        return database.db[
            self.COLLECTION_NAME
        ]

    # =========================================================
    # CREATE
    # =========================================================

    async def create(
        self,
        application: Application,
    ) -> Application:
        """
        Store a new application in MongoDB.
        """

        collection = self._get_collection()

        document = application.model_dump(
            mode="json"
        )

        await collection.insert_one(
            document
        )

        return application

    # =========================================================
    # GET BY ID
    # =========================================================

    async def get_by_id(
        self,
        application_id: str,
        user_id: str,
    ) -> Optional[Application]:
        """
        Retrieve an application belonging
        to the authenticated user.
        """

        collection = self._get_collection()

        document = await collection.find_one(
            {
                "id": application_id,
                "user_id": user_id,
            }
        )

        if not document:
            return None

        document.pop(
            "_id",
            None
        )

        return Application.model_validate(
            document
        )

    # =========================================================
    # LIST USER APPLICATIONS
    # =========================================================

    async def list_by_user(
        self,
        user_id: str,
    ) -> List[Application]:
        """
        Retrieve all applications belonging
        to the authenticated user.
        """

        collection = self._get_collection()

        cursor = collection.find(
            {
                "user_id": user_id,
            }
        ).sort(
            "updated_at",
            -1,
        )

        applications: List[Application] = []

        async for document in cursor:

            document.pop(
                "_id",
                None
            )

            applications.append(
                Application.model_validate(
                    document
                )
            )

        return applications

    # =========================================================
    # UPDATE
    # =========================================================

    async def update(
        self,
        application: Application,
    ) -> Application:
        """
        Update an existing application.
        """

        collection = self._get_collection()

        document = application.model_dump(
            mode="json"
        )

        result = await collection.replace_one(
            {
                "id": application.id,
                "user_id": application.user_id,
            },
            document,
        )

        if result.matched_count == 0:
            raise ValueError(
                "Application not found."
            )

        return application

    # =========================================================
    # DELETE
    # =========================================================

    async def delete(
        self,
        application_id: str,
        user_id: str,
    ) -> bool:
        """
        Delete an application belonging
        to the authenticated user.
        """

        collection = self._get_collection()

        result = await collection.delete_one(
            {
                "id": application_id,
                "user_id": user_id,
            }
        )

        return result.deleted_count > 0