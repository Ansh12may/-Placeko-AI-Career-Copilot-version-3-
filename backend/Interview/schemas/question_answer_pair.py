"""
Question Answer Pair Schema

Represents a complete interaction during an interview.

Each interaction consists of:

Question
        ↓
Candidate Answer
        ↓
AI Feedback

InterviewSession stores a list of these objects.
"""

from typing import Optional

from pydantic import BaseModel, Field

from backend.Interview.schemas.interview_question import InterviewQuestion
from backend.Interview.schemas.interview_answer import InterviewAnswer
from backend.Interview.schemas.interview_feedback import InterviewFeedback


class QuestionAnswerPair(BaseModel):
    """
    Represents one interview interaction.
    """

    question: InterviewQuestion = Field(
        ...,
        description="Interview question."
    )

    answer: Optional[InterviewAnswer] = Field(
        default=None,
        description="Candidate answer."
    )

    feedback: Optional[InterviewFeedback] = Field(
        default=None,
        description="AI evaluation of the answer."
    )

    interaction_completed: bool = Field(
    default=False,
    description="Whether the full question-answer-feedback cycle has finished."

)