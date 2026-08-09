from pydantic import BaseModel


class AuthResponse(BaseModel):
    success: bool
    message: str
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"