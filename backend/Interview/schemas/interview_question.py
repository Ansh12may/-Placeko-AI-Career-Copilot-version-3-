"""
Interview Question Schema

Represents a single interview question generated
during an AI mock interview.

This schema is shared across:

- Question Generator Agent
- Interview Session Agent
- Answer Evaluation Agent
- Follow-up Agent

It contains metadata required for asking and
evaluating the question.
"""

from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from backend.Interview.schemas.interview_plan import DifficultyLevel


# ==========================================================
# ENUMS
# ==========================================================

class QuestionCategory(str, Enum):
    """
    Category of interview question.
    """

    TECHNICAL = "Technical"

    BEHAVIORAL = "Behavioral"

    PROJECT = "Project"

    HR = "HR"

    SYSTEM_DESIGN = "System Design"


# ==========================================================
# SCHEMA
# ==========================================================

class InterviewQuestion(BaseModel):
    """
    Represents a single interview question.
    """

    question_id: int = Field(
        ...,
        ge=1,
        description="Sequential question number."
    )

    category: QuestionCategory = Field(
        ...,
        description="Interview question category."
    )

    difficulty: DifficultyLevel = Field(
        ...,
        description="Difficulty level."
    )

    question: str = Field(
        ...,
        description="Interview question."
    )

    focus_topic: str = Field(
        ...,
        description="Primary topic being evaluated."
    )

    expected_topics: List[str] = Field(
        default_factory=list,
        description=(
            "Key concepts expected in a good answer."
        )
    )

    followup_allowed: bool = Field(
        default=True,
        description=(
            "Whether follow-up questions are allowed."
        )
    )

    estimated_time_seconds: int = Field(
        default=120,
        ge=30,
        le=600,
        description="Recommended answer duration."
    )

    interviewer_notes: str = Field(
        default="",
        description=(
            "Hidden guidance for the interviewer."
        )
    )
    prerequisite_question_id: int | None = None