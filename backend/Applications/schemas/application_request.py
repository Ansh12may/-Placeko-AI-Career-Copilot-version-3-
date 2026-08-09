"""
Application Request Schemas

Defines request models used by the Application API.
"""

from typing import Optional

from pydantic import BaseModel, Field

from backend.Applications.schemas.application import (
    ApplicationStatus,
)


# =========================================================
# CREATE APPLICATION
# =========================================================

class ApplicationCreateRequest(BaseModel):
    """
    Request for creating a new job application.
    """

    job_id: Optional[str] = None

    job_title: str = Field(
        min_length=1,
        max_length=200,
    )

    company: str = Field(
        min_length=1,
        max_length=200,
    )

    location: Optional[str] = None

    apply_url: Optional[str] = None

    status: ApplicationStatus = (
        ApplicationStatus.SAVED
    )

    notes: Optional[str] = None


# =========================================================
# UPDATE STATUS
# =========================================================

class ApplicationStatusUpdateRequest(BaseModel):
    """
    Request for moving an application to another
    Kanban stage.
    """

    status: ApplicationStatus


# =========================================================
# UPDATE APPLICATION
# =========================================================

class ApplicationUpdateRequest(BaseModel):
    """
    Request for updating editable application details.
    """

    job_title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    company: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    location: Optional[str] = None

    apply_url: Optional[str] = None

    notes: Optional[str] = None

    status: Optional[ApplicationStatus] = None