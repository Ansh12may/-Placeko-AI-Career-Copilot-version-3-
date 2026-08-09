"""
Register Request Schema
Represents the request body received during user registration.
"""
from pydantic import BaseModel, EmailStr, Field
class RegisterRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's full name"
    )
    email: EmailStr = Field(
        ...,
        description="User email address"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="User password"
    )