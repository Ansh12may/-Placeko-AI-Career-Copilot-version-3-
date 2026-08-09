"""
Interview Session Schema

Represents a complete AI interview session.

This is the central object of the Interview Module
and acts as the single source of truth throughout
the interview lifecycle.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from backend.Resume.schemas.candidate import CandidateProfile
from backend.Jobs.schemas.job import Job
from backend.Interview.schemas.interview_report import InterviewReport
from backend.Interview.schemas.interview_plan import InterviewPlan
from backend.Interview.schemas.question_answer_pair import (
    QuestionAnswerPair,
)


# ==========================================================
# ENUM
# ==========================================================

class InterviewStatus(str, Enum):
    """
    Current state of the interview.
    """

    NOT_STARTED = "Not Started"

    IN_PROGRESS = "In Progress"

    PAUSED = "Paused"

    COMPLETED = "Completed"

    TERMINATED = "Terminated"


# ==========================================================
# SCHEMA
# ==========================================================

class InterviewSession(BaseModel):
    """
    Represents one complete interview session.
    """

    session_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique interview session ID."
    )

    user_id: str = Field(
        ...,
        description="ID of the authenticated user who owns the interview."
    )

    resume_id: str = Field(
        ...,
        description="ID of the resume used for this interview."
    )

    candidate: CandidateProfile = Field(
        ...,
        description="Candidate participating in the interview."
    )

    target_job: Optional[Job] = Field(
        default=None,
        description="Target job for the interview."
    )

    interview_plan: InterviewPlan = Field(
        ...,
        description="Interview blueprint."
    )

    history: List[QuestionAnswerPair] = Field(
        default_factory=list,
        description="Complete interview history."
    )

    current_question_index: int = Field(
        default=0,
        ge=0,
        description="Index of the current question."
    )

    status: InterviewStatus = Field(
        default=InterviewStatus.NOT_STARTED,
        description="Current interview status."
    )

    started_at: Optional[datetime] = Field(
        default=None,
        description="Interview start time."
    )

    ended_at: Optional[datetime] = Field(
        default=None,
        description="Interview end time."
    )

    report: Optional[InterviewReport] = Field(
        default=None,
        description="Final interview report."
    )