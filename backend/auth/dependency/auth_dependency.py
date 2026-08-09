"""
Authentication Dependency
Responsible for:
- Reading JWT from Authorization header
- Decoding JWT
- Fetching current user from MongoDB
Contains NO business logic.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from backend.auth.repositories.auth_repository import AuthRepository
from backend.auth.utils.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"

)
repository = AuthRepository()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    
    """
    Return the authenticated user.
    """
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    
    if payload.get("type") != "access":
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token."
    )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )

    user = await repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user

