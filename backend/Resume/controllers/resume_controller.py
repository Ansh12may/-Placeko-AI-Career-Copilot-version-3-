"""
Resume Controller

Responsible for:
- HTTP request validation
- Authentication dependency
- Calling ResumeService
- Returning API responses

Contains NO business logic.
"""

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from backend.Resume.services.resume_service import (
    ResumeService,
)

from backend.auth.dependency.auth_dependency import (
    get_current_user,
)


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"],
)


resume_service = ResumeService()


# =========================================================
# Upload Resume
# =========================================================

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    """
    Upload and analyze a resume.

    The controller only forwards the authenticated
    user and uploaded file to ResumeService.
    """

    return await resume_service.upload_resume(
        user_id=str(current_user["_id"]),
        file=file,
    )


# =========================================================
# Get All Resumes
# =========================================================

@router.get("")
async def get_resumes(
    current_user=Depends(get_current_user),
):
    """
    Return all resumes belonging to the authenticated user.
    """

    return await resume_service.get_user_resumes(
        user_id=str(current_user["_id"]),
    )


# =========================================================
# Get Single Resume
# =========================================================

@router.get("/{resume_id}")
async def get_resume(
    resume_id: str,
    current_user=Depends(get_current_user),
):
    """
    Return a specific resume belonging to the authenticated user.
    """

    return await resume_service.get_resume(
        user_id=str(current_user["_id"]),
        resume_id=resume_id,
    )


# =========================================================
# Set Active Resume
# =========================================================

@router.patch("/{resume_id}/active")
async def set_active_resume(
    resume_id: str,
    current_user=Depends(get_current_user),
):
    """
    Set a user's resume as the active resume.
    """

    return await resume_service.set_active_resume(
        user_id=str(current_user["_id"]),
        resume_id=resume_id,
    )


# =========================================================
# Delete Resume
# =========================================================

@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    current_user=Depends(get_current_user),
):
    """
    Delete a user's resume.
    """

    return await resume_service.delete_resume(
        user_id=str(current_user["_id"]),
        resume_id=resume_id,
    )