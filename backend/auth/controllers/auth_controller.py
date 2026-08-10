from fastapi import APIRouter
from backend.auth.services.auth_service import AuthService
from backend.auth.schemas.register_request import RegisterRequest
from backend.auth.schemas.login_request import LoginRequest
from fastapi import Depends
from backend.auth.dependency.auth_dependency import get_current_user
from backend.auth.schemas.refresh_request import RefreshRequest
from fastapi.responses import RedirectResponse
from backend.config.settings import settings

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)
auth_service = AuthService()

@router.post("/register")
async def register(request: RegisterRequest):
    return await auth_service.register(request)




@router.post("/login")
async def login(request: LoginRequest):
    return await auth_service.login(request)


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return {
        "success": True,
        "data": {
            "id": str(current_user["_id"]),
            "full_name": current_user["full_name"],
            "email": current_user["email"],
            "provider": current_user["provider"],
            "avatar": current_user.get("avatar"),
            "email_verified": current_user.get("email_verified", False)
        }

    }

@router.post("/refresh")
async def refresh(request: RefreshRequest):
    return await auth_service.refresh(request)


@router.post("/logout")
async def logout():
    return await auth_service.logout()


@router.get("/google")
async def google_login():
    """
    Redirect user to Google OAuth.
    """

    result = await auth_service.google_login()

    return RedirectResponse(
        url=result["authorization_url"]
    )


@router.get("/google/callback")
async def google_callback(
    code: str,
):
    """
    Google OAuth callback.
    """

    result = await auth_service.google_callback(
        code=code,
    )

    access_token = result["data"]["access_token"]
    refresh_token = result["data"]["refresh_token"]

    redirect_url = (
        f"{settings.FRONTEND_URL}"
        f"/oauth/callback"
        f"?access_token={access_token}"
        f"&refresh_token={refresh_token}"
    )

    return RedirectResponse(
        url=redirect_url
    )

