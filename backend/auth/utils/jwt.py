"""
JWT Utility
Responsible for:
- Creating Access Tokens
- Creating Refresh Tokens
- Decoding Token
Contains NO business logic.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from backend.config.settings import settings

def create_access_token(data: dict) -> str:
    """
    Create JWT access token.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """
    Create JWT refresh token.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload.update({"exp": expire})
    return jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)



def decode_token(token: str) -> dict:
    """
    Decode JWT token.
    Raises JWTError if invalid.
    """
    return jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ALGORITHM])