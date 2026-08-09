"""
Interview Answer Schema

Represents a single answer given by the candidate
during an interview.

This schema stores ONLY the candidate's response.
Evaluation is performed separately by the
Answer Evaluation Agent.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# ENUMS
# ==========================================================

class AnswerSource(str, Enum):
    """
    Specifies how the candidate answered.
    """

    TEXT = "Text"

    VOICE = "Voice"


# ==========================================================
# SCHEMA
# ==========================================================



class AnswerMetadata(BaseModel):
    audio_duration: float
    word_count: int
    speech_rate: float



class InterviewAnswer(BaseModel):
    """
    Represents a candidate's response
    to a single interview question.
    """

    question_id: int = Field(
        ...,
        ge=1,
        description="ID of the question being answered."
    )

    transcript: str = Field(
        ...,
        min_length=1,
        description="Text transcript of the candidate's answer."
    )

    source: AnswerSource = Field(
        default=AnswerSource.TEXT,
        description="Whether the answer was typed or spoken."
    )

    duration_seconds: float = Field(
        default=0,
        ge=0,
        description="Time taken by the candidate to answer."
    )

    answered_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the answer was submitted."
    )

    metadata: AnswerMetadata | None = None