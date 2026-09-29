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

    @property
    def collection(self):
        """
        Return the MongoDB users collection.
        """
        return database.db["users"]

    # Create User
   
    async def create_user(self,user: User) -> str:
        """
        Insert a new user into MongoDB.
        Returns:
            str: MongoDB inserted document ID.
        """
        # A Pydantic (v2) method that converts the User object into a
        # standard Python dictionary so MongoDB can store it as BSON/JSON.
        result = await self.collection.insert_one(
            #converts data from pydantic to standard python dictionary
            user.model_dump(    
                by_alias=True,
                exclude={"id"},
            )
        )
        return str(result.inserted_id)

    # Get User By Email
    async def get_user_by_email(self,email: str):

        return await self.collection.find_one(
            {
                "email": email,
            }
        )
    # Get User By ID

    async def get_user_by_id(self,user_id: str):
        """
        Find a user by MongoDB ObjectId.
        """
        return await self.collection.find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
    
    # Get User By Provider

    async def get_user_by_provider(self,provider: str,provider_id: str):
        return await self.collection.find_one(
            {
                "provider": provider,
                "provider_id": provider_id,
            }
        )

    # Update User
    async def update_user(self,user_id: str,update_data: dict):
        """
        Update fields of an existing user.
        """
        await self.collection.update_one(
            {
                "_id": ObjectId(user_id),
            },
            {
                "$set": update_data,
            },
        )
    # Delete User
    async def delete_user(self,user_id: str):
        """
        Delete a user by MongoDB ObjectId.
        """
        await self.collection.delete_one(
            {
                "_id": ObjectId(user_id),
            }
        )