"""
Google OAuth Utility
Responsible for:
- Building Google authorization URL
- Exchanging authorization code for Google tokens
- Fetching Google user information
"""

import httpx
from backend.config.settings import settings

GOOGLE_AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth"
)

GOOGLE_TOKEN_URL = (
    "https://oauth2.googleapis.com/token"
)

GOOGLE_USERINFO_URL = (
    "https://www.googleapis.com/oauth2/v2/userinfo"
)

def build_google_authorization_url() -> str:
    """
    Build the Google OAuth authorization URL.
    """

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }

    request = httpx.Request(
        "GET",
        GOOGLE_AUTH_URL,
        params=params,
    )

    return str(request.url)


async def exchange_google_code(
    code: str,
) -> dict:
    """
    Exchange Google authorization code
    for Google access token.
    """

    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            GOOGLE_TOKEN_URL,
            data=data,
        )

        response.raise_for_status()

        return response.json()


async def get_google_user(
    access_token: str,
) -> dict:
    """
    Fetch authenticated user's Google profile.
    """

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            GOOGLE_USERINFO_URL,
            headers=headers,
        )

        response.raise_for_status()

        return response.json()