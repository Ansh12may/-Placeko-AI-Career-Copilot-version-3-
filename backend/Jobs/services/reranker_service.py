"""
Reranker Service

Responsible for reranking retrieved jobs using
a CrossEncoder model.

Responsibilities:
- Convert candidate and jobs into text
- Create resume/job pairs
- Call RerankerTool
- Sort jobs by relevance
- Return Top-K jobs

This service performs NO:
- Vector database operations
- Job retrieval
- LLM reasoning
- Business-level recommendation decisions
"""

from typing import List

from backend.Jobs.schemas.job import Job
from backend.Jobs.tools.reranker_tool import (
    RerankerTool,
)

from backend.Resume.schemas.candidate import (
    CandidateProfile,
)

from backend.utils.text_formatter import (
    resume_to_text,
    job_to_text,
)


class RerankerService:
    """
    Service responsible for second-stage job reranking
    using a CrossEncoder model.
    """

    def __init__(self):
        self.reranker = RerankerTool()

    def rerank(
        self,
        candidate_profile: CandidateProfile,
        jobs: List[Job],
        top_k: int = 10,
    ) -> List[Job]:
        """
        Rerank candidate jobs using CrossEncoder relevance.

        Pipeline:

        CandidateProfile
              +
        Retrieved Jobs
              ↓
        Text representations
              ↓
        CrossEncoder
              ↓
        Relevance scores
              ↓
        Sorted jobs
              ↓
        Top-K
        """

        if not jobs:
            return []

        # -----------------------------------------------------
        # Candidate representation
        # -----------------------------------------------------

        resume_text = resume_to_text(
            candidate_profile
        )

        # -----------------------------------------------------
        # Job representations
        # -----------------------------------------------------

        job_texts = [
            job_to_text(job)
            for job in jobs
        ]

        # -----------------------------------------------------
        # CrossEncoder scoring
        # -----------------------------------------------------

        scores = self.reranker.score_batch(
            resume_text=resume_text,
            job_texts=job_texts,
        )

        # -----------------------------------------------------
        # Pair jobs with scores
        # -----------------------------------------------------

        scored_jobs = list(
            zip(
                jobs,
                scores,
            )
        )

        # -----------------------------------------------------
        # Sort by relevance
        # -----------------------------------------------------

        scored_jobs.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        # -----------------------------------------------------
        # Return Top-K
        # -----------------------------------------------------

        return [
            job
            for job, _ in scored_jobs[:top_k]
        ]