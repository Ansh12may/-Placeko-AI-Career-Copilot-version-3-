"""
Auth Service

Responsible for:
- User Registration
- User Login
- Refresh Token
- OAuth Authentication
- Google Authentication
- GitHub Authentication
- JWT Token Generation

This service contains ALL authentication business logic.

OAuth provider-specific HTTP communication is handled
by provider utilities. This service receives normalized
provider information and creates or authenticates the
corresponding user.
"""

from datetime import datetime, timezone

from fastapi import HTTPException, status
from jose import JWTError

from backend.auth.models.user import (
    User,
    AuthProvider,
)

from backend.auth.repositories.auth_repository import (
    AuthRepository,
)

from backend.auth.utils.password import (
    hash_password,
    verify_password,
)

from backend.auth.utils.jwt import (
    decode_token,
    create_access_token,
    create_refresh_token,
)

from backend.auth.utils.google_oauth import (
    build_google_authorization_url,
    exchange_google_code,
    get_google_user,
)


class AuthService:

    def __init__(self):
        self.repository = AuthRepository()

    # =========================================================
    # JWT TOKEN GENERATION
    # =========================================================

    def _generate_tokens(
        self,
        user_id: str,
        email: str,
    ):
        """
        Generate JWT access and refresh tokens.

        Both normal email authentication and OAuth
        authentication use this same method.
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

    # =========================================================
    # EMAIL REGISTRATION
    # =========================================================

    async def register(
        self,
        request,
    ):
        """
        Register a new email/password user.
        """

        existing_user = (
            await self.repository.get_user_by_email(
                request.email
            )
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists.",
            )

        password_hash = hash_password(
            request.password
        )

        now = datetime.now(
            timezone.utc
        )

        user = User(
            full_name=request.full_name,
            email=request.email,
            password_hash=password_hash,
            provider=AuthProvider.EMAIL,
            provider_id=None,
            avatar=None,
            email_verified=False,
            created_at=now,
            updated_at=now,
        )

        user_id = (
            await self.repository.create_user(
                user
            )
        )

        access_token, refresh_token = (
            self._generate_tokens(
                user_id=user_id,
                email=user.email,
            )
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

    # =========================================================
    # EMAIL LOGIN
    # =========================================================

    async def login(
        self,
        request,
    ):
        """
        Login an existing email/password user.
        """

        user = (
            await self.repository.get_user_by_email(
                request.email
            )
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        provider = user.get(
            "provider",
            AuthProvider.EMAIL.value,
        )

        if provider != AuthProvider.EMAIL.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"This account uses {provider} login."
                ),
            )

        password_hash = user.get(
            "password_hash"
        )

        if not password_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This account does not have a password.",
            )

        if not verify_password(
            request.password,
            password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        access_token, refresh_token = (
            self._generate_tokens(
                user_id=str(user["_id"]),
                email=user["email"],
            )
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

    # =========================================================
    # GENERIC OAUTH AUTHENTICATION
    # =========================================================

    async def authenticate_oauth(
        self,
        provider: AuthProvider,
        provider_id: str,
        email: str,
        full_name: str,
        avatar: str | None = None,
        email_verified: bool = True,
    ):
        """
        Authenticate a user through an OAuth provider.

        Supports:

        Google
        GitHub

        Flow:

            Provider profile
                    ↓
            Find provider account
                    ↓
              Existing user?
                /       \
              yes       no
               ↓         ↓
             Login    Check email
                         ↓
                   Create account
                         ↓
                    Generate JWT
        """

        # =====================================================
        # 1. Validate provider
        # =====================================================

        if provider not in {
            AuthProvider.GOOGLE,
            AuthProvider.GITHUB,
        }:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported OAuth provider.",
            )

        # =====================================================
        # 2. Validate provider ID
        # =====================================================

        if not provider_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OAuth provider ID is required.",
            )

        # =====================================================
        # 3. Find existing OAuth user
        # =====================================================

        existing_oauth_user = (
            await self.repository.get_user_by_provider(
                provider=provider.value,
                provider_id=provider_id,
            )
        )

        # =====================================================
        # 4. Existing OAuth user
        # =====================================================

        if existing_oauth_user:

            update_data = {
                "updated_at": datetime.now(
                    timezone.utc
                ),
            }

            if avatar:
                update_data["avatar"] = avatar

            if full_name:
                update_data["full_name"] = full_name

            if email_verified:
                update_data["email_verified"] = True

            await self.repository.update_user(
                user_id=str(
                    existing_oauth_user["_id"]
                ),
                update_data=update_data,
            )

            access_token, refresh_token = (
                self._generate_tokens(
                    user_id=str(
                        existing_oauth_user["_id"]
                    ),
                    email=existing_oauth_user[
                        "email"
                    ],
                )
            )

            return {
                "success": True,
                "message": (
                    f"{provider.value.capitalize()} "
                    "login successful."
                ),
                "data": {
                    "user_id": str(
                        existing_oauth_user["_id"]
                    ),
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            }

        # =====================================================
        # 5. Check whether email already exists
        # =====================================================

        existing_email_user = (
            await self.repository.get_user_by_email(
                email
            )
        )

        if existing_email_user:

            existing_provider = existing_email_user.get(
                "provider",
                AuthProvider.EMAIL.value,
            )

            # -------------------------------------------------
            # Email/password account already exists
            # -------------------------------------------------

            if existing_provider == AuthProvider.EMAIL.value:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        "An account with this email already "
                        "exists. Please log in using email "
                        "and password."
                    ),
                )

            # -------------------------------------------------
            # Another OAuth provider owns this email
            # -------------------------------------------------

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "This email is already associated "
                    f"with {existing_provider} authentication."
                ),
            )

        # =====================================================
        # 6. Create new OAuth user
        # =====================================================

        now = datetime.now(
            timezone.utc
        )

        user = User(
            full_name=full_name,
            email=email,
            password_hash=None,
            provider=provider,
            provider_id=provider_id,
            avatar=avatar,
            email_verified=email_verified,
            created_at=now,
            updated_at=now,
        )

        user_id = (
            await self.repository.create_user(
                user
            )
        )

        # =====================================================
        # 7. Generate Placeko JWT
        # =====================================================

        access_token, refresh_token = (
            self._generate_tokens(
                user_id=user_id,
                email=email,
            )
        )

        return {
            "success": True,
            "message": (
                f"{provider.value.capitalize()} "
                "registration successful."
            ),
            "data": {
                "user_id": user_id,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        }

    # =========================================================
    # GOOGLE LOGIN
    # =========================================================

    async def google_login(self):
        """
        Generate the Google OAuth authorization URL.
        """

        return {
            "success": True,
            "authorization_url":
                build_google_authorization_url(),
        }

    # =========================================================
    # GOOGLE CALLBACK
    # =========================================================

    async def google_callback(
        self,
        code: str,
    ):
        """
        Handle Google's OAuth callback.

        Flow:

        Google authorization code
                ↓
        Exchange code for Google token
                ↓
        Fetch Google profile
                ↓
        normalize profile
                ↓
        authenticate_oauth()
                ↓
        MongoDB
                ↓
        Placeko JWT
        """

        # -----------------------------------------------------
        # 1. Exchange authorization code
        # -----------------------------------------------------

        try:

            token_data = await exchange_google_code(
                code
            )

        except Exception as error:

            print(
                "Google token exchange failed:",
                error,
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google authentication failed.",
            )

        google_access_token = (
            token_data.get("access_token")
        )

        if not google_access_token:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=(
                    "Google access token was not returned."
                ),
            )

        # -----------------------------------------------------
        # 2. Fetch Google user profile
        # -----------------------------------------------------

        try:

            google_user = await get_google_user(
                google_access_token
            )

        except Exception as error:

            print(
                "Failed to fetch Google user:",
                error,
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=(
                    "Unable to retrieve Google account "
                    "information."
                ),
            )

        # -----------------------------------------------------
        # 3. Extract Google profile
        # -----------------------------------------------------

        google_id = google_user.get(
            "id"
        )

        email = google_user.get(
            "email"
        )

        full_name = (
            google_user.get("name")
            or google_user.get("email")
            or "Google User"
        )

        avatar = google_user.get(
            "picture"
        )

        email_verified = google_user.get(
            "verified_email",
            False,
        )

        if not google_id or not email:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Google account information "
                    "is incomplete."
                ),
            )

        # -----------------------------------------------------
        # 4. Delegate user authentication to generic OAuth
        # -----------------------------------------------------

        return await self.authenticate_oauth(
            provider=AuthProvider.GOOGLE,
            provider_id=google_id,
            email=email,
            full_name=full_name,
            avatar=avatar,
            email_verified=email_verified,
        )

    # =========================================================
    # REFRESH TOKEN
    # =========================================================

    async def refresh(
        self,
        request,
    ):
        """
        Generate new JWT tokens using a refresh token.
        """

        try:

            payload = decode_token(
                request.refresh_token
            )

        except JWTError:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=(
                    "Invalid or expired refresh token."
                ),
            )

        if payload.get("type") != "refresh":

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        user_id = payload.get(
            "sub"
        )

        if not user_id:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        user = (
            await self.repository.get_user_by_id(
                user_id
            )
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        access_token, refresh_token = (
            self._generate_tokens(
                user_id=str(user["_id"]),
                email=user["email"],
            )
        )

        return {
            "success": True,
            "message": (
                "Token refreshed successfully."
            ),
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        }

    # =========================================================
    # LOGOUT
    # =========================================================

    async def logout(self):
        """
        Logout the current user.

        JWT authentication is stateless, so the backend does
        not store or invalidate tokens.

        The frontend removes the access and refresh tokens.
        """

        return {
            "success": True,
            "message": "Logged out successfully.",
        }