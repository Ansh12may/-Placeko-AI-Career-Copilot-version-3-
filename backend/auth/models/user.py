"""
User Model
Represents a user document stored in MongoDB.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr,Field
from enum import Enum


class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    GITHUB = "github"


#Optional[str] means string or None
#filed means if user does not provide id mark as none
class User(BaseModel):
    id: Optional[str] = Field(default=None,alias="_id")
    full_name: str
    email: EmailStr
    password_hash: Optional[str] = None
    provider: AuthProvider = AuthProvider.EMAIL
    provider_id: Optional[str] = None
    avatar: Optional[str] = None
    email_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


    class Config:
        populate_by_name = True


