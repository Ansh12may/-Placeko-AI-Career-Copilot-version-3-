"""
Job Readiness / Evidence Schema

Maps explicit job requirements to evidence in the grounded
CandidateProfile. This is intentionally separate from the
CrossEncoder ranking score: ranking answers "which job is more
relevant?", while readiness answers "what does the candidate
actually prove for this job?".
"""

from typing import List, Literal
from pydantic import BaseModel, Field


RequirementStatus = Literal[
    "proven",
    "unproven",
    "resume_gap",
    "candidate_confirmed",
]


class CandidateEvidence(BaseModel):
    source_type: Literal[
        "skill",
        "project",
        "experience",
        "certification",
        "candidate_confirmation",
    ]
    source: str
    matched_text: str | None = None


class JobRequirementEvidence(BaseModel):
    requirement: str
    status: RequirementStatus
    evidence: List[CandidateEvidence] = Field(default_factory=list)
    explanation: str


class JobReadiness(BaseModel):
    """
    Explainable requirement-to-evidence mapping for one job.

    `resume_gap` means the requirement is explicitly required by
    the job but is not evidenced by the current resume/profile.
    It does NOT claim the candidate lacks the skill.
    """

    requirements: List[JobRequirementEvidence] = Field(default_factory=list)
    proven_count: int = 0
    unproven_count: int = 0
    resume_gap_count: int = 0
    candidate_confirmed_count: int = 0
