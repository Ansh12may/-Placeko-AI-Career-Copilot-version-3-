"""
Auth Service
Responsible for:
- User Registration
- User Login
- Refresh Token
- Google Authentication
- GitHub Authentication
This service contains ALL authentication business logic.
"""

from datetime import datetime, timezone
from fastapi import HTTPException, status
from jose import JWTError
from backend.auth.models.user import User, AuthProvider
from backend.auth.repositories.auth_repository import AuthRepository
from backend.auth.utils.password import hash_password, verify_password
from backend.auth.utils.jwt import (
    decode_token,
    create_access_token,
    create_refresh_token,
)

class AuthService:
    def __init__(self):
        self.repository = AuthRepository()

    def _generate_tokens(self, user_id: str, email: str):
        """
        Generate JWT access and refresh tokens.
        """
        access_token = create_access_token(
            {
                "sub": user_id,
                "email": email,
                "type": "access",
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": user_id,
                "type": "refresh",
            }
        )
        return access_token, refresh_token

    async def register(self, request):
        """
        Register a new user.
        """
        # Check if email already exists
        existing_user = await self.repository.get_user_by_email(
            request.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists."
            )

        # Hash password
        password_hash = hash_password(request.password)

        # Create user
        user = User(
            full_name=request.full_name,
            email=request.email,
            password_hash=password_hash,
            provider=AuthProvider.EMAIL,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        user_id = await self.repository.create_user(user)

        access_token, refresh_token = self._generate_tokens(
            user_id=user_id,
            email=user.email,
        )

        return {
            "success": True,
            "message": "Registration successful.",
            "data": {
                "user_id": user_id,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        }

    async def login(self, request):
        """
        Login an existing user.
        """

        user = await self.repository.get_user_by_email(
            request.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        # Prevent password login for OAuth users
        if user.get("provider") != AuthProvider.EMAIL.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"This account uses {user['provider']} login."
            )

        # Verify password
        if not verify_password(
            request.password,
            user["password_hash"]
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        access_token, refresh_token = self._generate_tokens(
            user_id=str(user["_id"]),
            email=user["email"],
        )

        return {
            "success": True,
            "message": "Login successful.",
            "data": {
                "user_id": str(user["_id"]),
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        }

    async def refresh(self, request):
        """
        Generate new JWT tokens using a refresh token.
        """

        try:
            payload = decode_token(request.refresh_token)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token."
            )

        # Ensure this is actually a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token."
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token."
            )

        user = await self.repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        access_token, refresh_token = self._generate_tokens(
            user_id=str(user["_id"]),
            email=user["email"],
        )

        return {
            "success": True,
            "message": "Token refreshed successfully.",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        }

async def logout(self):
    """
    Logout the current user.
    Since JWT authentication is stateless, the backend
    does not store or invalidate tokens. The frontend
    is responsible for deleting the access and refresh
    tokens from storage.
    """
    return {
        "success": True,
        "message": "Logged out successfully."
    }