"""
Application Controller

FastAPI routes for the job application tracker.

The controller is responsible for:
- HTTP request handling
- Authentication
- Calling ApplicationService
- HTTP response formatting

Business logic belongs to ApplicationService.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from backend.Applications.schemas.application import (
    Application,
)

from backend.Applications.schemas.application_request import (
    ApplicationCreateRequest,
    ApplicationStatusUpdateRequest,
    ApplicationUpdateRequest,
)

from backend.Applications.services.application_service import (
    ApplicationService,
)

from backend.auth.dependency.auth_dependency import (
    get_current_user,
)


router = APIRouter(
    prefix="/api/applications",
    tags=["Applications"],
)


application_service = ApplicationService()


# =========================================================
# CREATE APPLICATION
# =========================================================

@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
async def create_application(
    request: ApplicationCreateRequest,
    current_user=Depends(get_current_user),
):
    """
    Create a new job application.
    """

    try:
        user_id = str(
            current_user["_id"]
        )

        application = (
            await application_service.create_application(
                request=request,
                user_id=user_id,
            )
        )

        return {
            "success": True,
            "data": application,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# GET ALL APPLICATIONS
# =========================================================

@router.get(
    "",
    response_model=dict,
)
async def get_applications(
    current_user=Depends(get_current_user),
):
    """
    Retrieve all applications belonging to
    the authenticated user.
    """

    try:
        user_id = str(
            current_user["_id"]
        )

        applications = (
            await application_service.get_applications(
                user_id=user_id,
            )
        )

        return {
            "success": True,
            "data": applications,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# GET APPLICATION BY ID
# =========================================================

@router.get(
    "/{application_id}",
    response_model=dict,
)
async def get_application(
    application_id: str,
    current_user=Depends(get_current_user),
):
    """
    Retrieve one application.
    """

    try:
        user_id = str(
            current_user["_id"]
        )

        application = (
            await application_service.get_application(
                application_id=application_id,
                user_id=user_id,
            )
        )

        return {
            "success": True,
            "data": application,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# UPDATE APPLICATION
# =========================================================

@router.patch(
    "/{application_id}",
    response_model=dict,
)
async def update_application(
    application_id: str,
    request: ApplicationUpdateRequest,
    current_user=Depends(get_current_user),
):
    """
    Update application details.
    """

    try:
        user_id = str(
            current_user["_id"]
        )

        application = (
            await application_service.update_application(
                application_id=application_id,
                request=request,
                user_id=user_id,
            )
        )

        return {
            "success": True,
            "data": application,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# UPDATE STATUS
# =========================================================

@router.patch(
    "/{application_id}/status",
    response_model=dict,
)
async def update_application_status(
    application_id: str,
    request: ApplicationStatusUpdateRequest,
    current_user=Depends(get_current_user),
):
    """
    Move an application to another Kanban stage.
    """

    try:
        user_id = str(
            current_user["_id"]
        )

        application = (
            await application_service.update_status(
                application_id=application_id,
                request=request,
                user_id=user_id,
            )
        )

        return {
            "success": True,
            "data": application,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# DELETE APPLICATION
# =========================================================

@router.delete(
    "/{application_id}",
    response_model=dict,
)
async def delete_application(
    application_id: str,
    current_user=Depends(get_current_user),
):
    """
    Delete an application.
    """

    try:
        user_id = str(
            current_user["_id"]
        )

        await application_service.delete_application(
            application_id=application_id,
            user_id=user_id,
        )

        return {
            "success": True,
            "message": "Application deleted successfully.",
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )