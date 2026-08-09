"""
Application Schemas

Defines the domain models used by the application tracking
and Kanban workflow.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# =========================================================
# APPLICATION STATUS
# =========================================================

class ApplicationStatus(str, Enum):
    """
    Current stage of a job application.
    """

    SAVED = "saved"

    APPLIED = "applied"

    SCREENING = "screening"

    INTERVIEW = "interview"

    OFFER = "offer"

    ACCEPTED = "accepted"

    REJECTED = "rejected"

    WITHDRAWN = "withdrawn"


# =========================================================
# APPLICATION
# =========================================================

class Application(BaseModel):
    """
    Represents one job application belonging to a user.
    """

    id: str

    user_id: str

    # -----------------------------------------------------
    # Job information
    # -----------------------------------------------------

    job_id: Optional[str] = None

    job_title: str

    company: str

    location: Optional[str] = None

    apply_url: Optional[str] = None

    # -----------------------------------------------------
    # Application state
    # -----------------------------------------------------

    status: ApplicationStatus = (
        ApplicationStatus.SAVED
    )

    # -----------------------------------------------------
    # User notes
    # -----------------------------------------------------

    notes: Optional[str] = None

    # -----------------------------------------------------
    # Dates
    # -----------------------------------------------------

    applied_at: Optional[datetime] = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )