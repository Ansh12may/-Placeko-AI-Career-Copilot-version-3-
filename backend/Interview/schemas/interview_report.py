"""
Interview Report Schema

Represents the final report generated after an AI interview.

This report summarizes the candidate's overall performance,
strengths, weaknesses, detailed feedback, and learning roadmap.
"""

from typing import List

from pydantic import BaseModel, Field

from enum import Enum

class HiringRecommendation(str, Enum):

    STRONG_HIRE = "Strong Hire"

    HIRE = "Hire"

    BORDERLINE = "Borderline"

    NO_HIRE = "No Hire"


# ==========================================================
# SCORE
# ==========================================================

class InterviewScore(BaseModel):
    """
    Represents an interview score.
    """

    score: float = Field(
        ...,
        ge=0,
        le=10,
        description="Score achieved."
    )

    max_score: float = Field(
        default=10,
        description="Maximum possible score."
    )


# ==========================================================
# QUESTION SUMMARY
# ==========================================================

class QuestionSummary(BaseModel):
    """
    Summary of an individual interview question.
    """

    question: str = Field(
        ...,
        description="Interview question."
    )

    score: float = Field(
        ...,
        ge=0,
        le=10,
        description="Overall score for this question."
    )

    strengths: List[str] = Field(
        default_factory=list,
        description="Strong aspects of the answer."
    )

    weaknesses: List[str] = Field(
        default_factory=list,
        description="Weak areas in the answer."
    )


# ==========================================================
# MAIN REPORT
# ==========================================================

class InterviewReport(BaseModel):
    """
    Final interview report.
    """

    overall_score: InterviewScore = Field(
        ...,
        description="Overall interview performance."
    )

    technical_score: InterviewScore = Field(
        ...,
        description="Technical performance."
    )

    communication_score: InterviewScore = Field(
        ...,
        description="Communication performance."
    )

    confidence_score: InterviewScore = Field(
        ...,
        description="Confidence score."
    )

    completeness_score: InterviewScore = Field(
        ...,
        description="Completeness score."
    )

    strengths: List[str] = Field(
        default_factory=list,
        description="Overall strengths."
    )

    weaknesses: List[str] = Field(
        default_factory=list,
        description="Overall weaknesses."
    )

    knowledge_gaps: List[str] = Field(
        default_factory=list,
        description="Important concepts the candidate should revise."
    )

    recommendations: List[str] = Field(
        default_factory=list,
        description="Personalized recommendations."
    )

    learning_roadmap: List[str] = Field(
        default_factory=list,
        description="Suggested learning roadmap."
    )

    question_summaries: List[QuestionSummary] = Field(
        default_factory=list,
        description="Performance for each interview question."
    )

    # hiring_recommendation: str = Field(
    #     ...,
    #     description="Overall hiring recommendation."
    # )

    final_feedback: str = Field(
        ...,
        description="Overall interview summary."
    )
    hiring_recommendation: HiringRecommendation