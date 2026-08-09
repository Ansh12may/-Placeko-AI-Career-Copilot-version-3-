from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class InterviewType(str, Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    MIXED = "mixed"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class InterviewRequest(BaseModel):
    """
    Request schema for starting a new interview.
    Sent from the frontend to the backend.
    """

  
    resume_id: str = Field(
        ...,
        description="Unique identifier of the parsed resume."
    )

    job_id: Optional[str] = Field(
        default=None,
        description="Optional job identifier if interviewing for a specific job."
    )

    job_description: Optional[str] = Field(
        default=None,
        description="Job description provided by the user if no job_id is available."
    )

    interview_type: InterviewType = Field(
    default=InterviewType.TECHNICAL,
    description="Type of interview (technical, behavioral, mixed)."

)
    difficulty: Difficulty = Field(
    default=Difficulty.MEDIUM,
    description="Interview difficulty (easy, medium, hard)."

)
    num_questions: int = Field(
        default=10,
        ge=1,
        le=30,
        description="Number of questions to generate."
    )

    include_projects: bool = Field(
        default=True,
        description="Whether to ask questions based on resume projects."
    )

    include_experience: bool = Field(
        default=True,
        description="Whether to ask questions based on work experience."
    )

    include_behavioral: bool = Field(
        default=True,
        description="Whether to include behavioral questions."
    )

    include_voice_analysis: bool = Field(
        default=False,
        description="Enable voice analysis if using voice interview."
    )