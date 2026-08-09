"""
Auth Repository
Responsible for:
- User CRUD operations
- MongoDB interactions
This repository performs NO business logic.
"""
from bson import ObjectId
from backend.database.db import database
from backend.auth.models.user import User

class AuthRepository:
    @property   #@property is a Python decorator that lets you call a method like an attribute.
    def collection(self):
        return database.db["users"]

    async def create_user(self, user: User) -> str:
        """
        Insert a new user into MongoDB.
        Returns the inserted document ID.
        """
        result = await self.collection.insert_one(
            user.model_dump(by_alias=True, exclude={"id"})
        )
        return str(result.inserted_id)

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one(
            {"email": email}
        )

    async def get_user_by_id(self, user_id: str):
        """
        Find a user by MongoDB ObjectId.
        """
        return await self.collection.find_one(
            {"_id": ObjectId(user_id)}
        )

    async def update_user(self, user_id: str, update_data: dict):
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )

    async def delete_user(self, user_id: str):
        await self.collection.delete_one(
            {"_id": ObjectId(user_id)}
        )