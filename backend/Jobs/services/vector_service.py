"""
Vector Service

Responsible for:
- Converting Job objects into searchable text
- Generating job embeddings
- Storing job vectors in Pinecone
- Converting Pinecone results back into Job objects
- Retrieving semantically similar jobs for a candidate

This service performs NO:
- LLM reasoning
- CrossEncoder reranking
- Business-level recommendation decisions
"""

from typing import List
import hashlib
import json

from backend.Jobs.schemas.job import Job
from backend.Resume.schemas.candidate import CandidateProfile

from backend.Jobs.tools.embedding_tool import EmbeddingTool
from backend.Jobs.tools.pinecone_tool import PineconeTool

from backend.utils.text_formatter import (
    job_to_text,
    resume_to_text,
)


class VectorService:
    """
    Service responsible for vector storage and
    first-stage semantic job retrieval.
    """

    def __init__(self):
        self.embedding_tool = EmbeddingTool()
        self.pinecone_tool = PineconeTool()

    # =========================================================
    # Store Jobs
    # =========================================================

    def store_jobs(
        self,
        jobs: List[Job],
    ) -> None:
        """
        Convert jobs into embeddings and store them in Pinecone.

        Embeddings are generated in batch to reduce repeated
        model/API calls.
        """

        if not jobs:
            return

        # -----------------------------------------------------
        # 1. Convert jobs → searchable text
        # -----------------------------------------------------

        job_texts = [
            job_to_text(job)
            for job in jobs
        ]

        # -----------------------------------------------------
        # 2. Generate embeddings
        # -----------------------------------------------------

        embeddings = self.embedding_tool.get_embeddings(
            job_texts
        )

        if not embeddings:
            return

        # -----------------------------------------------------
        # 3. Build Pinecone vectors
        # -----------------------------------------------------

        vectors = []

        for job, embedding in zip(
            jobs,
            embeddings,
        ):

            if not embedding:
                continue

            # -------------------------------------------------
            # Stable vector ID
            #
            # Prefer the application URL because it normally
            # identifies a specific job posting.
            #
            # Fall back to job fields when apply_url is absent.
            # -------------------------------------------------

            job_identity = (
                str(job.apply_url)
                if job.apply_url
                else (
                    f"{job.title}|"
                    f"{job.company}|"
                    f"{job.location}|"
                    f"{job.description}"
                )
            )

            vector_id = hashlib.sha256(
                job_identity.encode("utf-8")
            ).hexdigest()

            # -------------------------------------------------
            # Store complete Job in metadata
            # -------------------------------------------------

            vectors.append(
                {
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "job": json.dumps(
                            job.model_dump(
                                mode="json"
                            )
                        ),
                    },
                }
            )

        # -----------------------------------------------------
        # 4. Upsert into Pinecone
        # -----------------------------------------------------

        if vectors:
            self.pinecone_tool.upsert_vectors(
                vectors
            )

    # =========================================================
    # Search By Candidate
    # =========================================================

    def search_by_candidate(
        self,
        candidate_profile: CandidateProfile,
        top_k: int = 20,
    ) -> List[Job]:
        """
        Retrieve semantically similar jobs for a candidate.

        Pipeline:

        CandidateProfile
              ↓
        resume_to_text()
              ↓
        EmbeddingTool
              ↓
        Candidate Vector
              ↓
        Pinecone
              ↓
        Top-N Matches
              ↓
        Deduplication
              ↓
        Job objects
        """

        # -----------------------------------------------------
        # 1. Candidate → semantic text
        # -----------------------------------------------------

        resume_text = resume_to_text(
            candidate_profile
        )

        # -----------------------------------------------------
        # 2. Candidate → embedding
        # -----------------------------------------------------

        embedding = self.embedding_tool.get_embedding(
            resume_text
        )

        if not embedding:
            return []

        # -----------------------------------------------------
        # 3. Semantic vector search
        # -----------------------------------------------------

        matches = self.pinecone_tool.query_vectors(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
        )

        # -----------------------------------------------------
        # 4. Convert Pinecone matches → Job objects
        # -----------------------------------------------------

        jobs: List[Job] = []
        seen_jobs = set()

        for match in matches:

            metadata = match.metadata or {}

            job_data = metadata.get("job")

            if not job_data:
                continue

            try:

                if isinstance(job_data, str):
                    job_data = json.loads(job_data)

                job = Job.model_validate(
                    job_data
                )

                # -------------------------------------------------
                # Deduplicate job postings
                #
                # Prefer apply_url as the job identity.
                # Fall back to title/company/location.
                # -------------------------------------------------

                identity = (
                    str(job.apply_url)
                    if job.apply_url
                    else (
                        f"{job.title}|"
                        f"{job.company}|"
                        f"{job.location}"
                    )
                )

                if identity in seen_jobs:
                    continue

                seen_jobs.add(identity)

                # -------------------------------------------------
                # Preserve semantic similarity score
                #
                # This is the similarity score returned by
                # Pinecone. It is NOT a percentage.
                # -------------------------------------------------

                if hasattr(match, "score"):
                    job.match_score = match.score

                jobs.append(job)

            except Exception:
                # Ignore malformed metadata rather than
                # breaking the complete recommendation pipeline.
                continue

        return jobs

    # =========================================================
    # Generic Semantic Search
    # =========================================================

    def search(
        self,
        query: str,
        top_k: int = 20,
    ):
        """
        Generic semantic search.

        Primarily useful for testing or future search features.

        RecommendationAgent should use search_by_candidate()
        when generating personalized job recommendations.
        """

        embedding = self.embedding_tool.get_embedding(
            query
        )

        if not embedding:
            return []

        return self.pinecone_tool.query_vectors(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
        )