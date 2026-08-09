"""
Interview Plan Schema

Represents the blueprint for a personalized AI mock interview.

The Interview Planner Agent generates this plan based on the
candidate profile, target job, and interview configuration.

The plan determines the structure of the interview but DOES NOT
contain the actual interview questions.
"""

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


# ==========================================================
# ENUMS
# ==========================================================

class InterviewMode(str, Enum):
    """
    Type of interview to conduct.
    """

    MIXED = "Mixed"

    TECHNICAL = "Technical"

    BEHAVIORAL = "Behavioral"

    PROJECT = "Project"

    HR = "HR"


class DifficultyLevel(str, Enum):
    """
    Difficulty level of interview.
    """

    EASY = "Easy"

    MEDIUM = "Medium"

    HARD = "Hard"


# ==========================================================
# SCHEMA
# ==========================================================

class InterviewPlan(BaseModel):
    """
    Blueprint of an interview session.
    """

    interview_mode: InterviewMode = Field(
        ...,
        description="Type of interview."
    )

    difficulty: DifficultyLevel = Field(
        ...,
        description="Overall interview difficulty."
    )

    duration_minutes: int = Field(
        ...,
        ge=10,
        le=90,
        description="Expected interview duration."
    )

    technical_questions: int = Field(
        ...,
        ge=0,
        description="Number of technical questions."
    )

    behavioral_questions: int = Field(
        ...,
        ge=0,
        description="Number of behavioral questions."
    )

    project_questions: int = Field(
        ...,
        ge=0,
        description="Number of project-based questions."
    )

    followup_questions: int = Field(
        ...,
        ge=0,
        description="Maximum follow-up questions."
    )

    focus_topics: List[str] = Field(
        default_factory=list,
        description="Topics to emphasize during the interview."
    )

    evaluation_criteria: List[str] = Field(
        default_factory=list,
        description="Criteria used to evaluate candidate responses."
    )

    interviewer_notes: str = Field(
        ...,
        description=(
            "Instructions for the Interview Session Agent "
            "on how the interview should be conducted."
        )
    )