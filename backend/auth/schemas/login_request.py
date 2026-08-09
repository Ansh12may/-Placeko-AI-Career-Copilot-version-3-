from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):

    email: EmailStr = Field(
        ...,
        description="User email"
    )

    password: str = Field(
        ...,
        description="User password"
    )