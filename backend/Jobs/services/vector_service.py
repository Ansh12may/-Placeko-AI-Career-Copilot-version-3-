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
        """

        if not jobs:
            return

        vectors = []

        for job in jobs:

            # -------------------------------------------------
            # Job → searchable semantic text
            # -------------------------------------------------

            text = job_to_text(job)

            # -------------------------------------------------
            # Generate embedding
            # -------------------------------------------------

            embedding = self.embedding_tool.get_embedding(
                text
            )

            if not embedding:
                continue

            # -------------------------------------------------
            # Generate stable Pinecone vector ID
            #
            # Job schema currently has no unique ID, so we
            # derive one from the job's identifying fields.
            # -------------------------------------------------

            vector_id = hashlib.sha256(
                (
                    f"{job.title}|"
                    f"{job.company}|"
                    f"{job.location}"
                ).encode("utf-8")
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
                        )
                    },
                }
            )

        # -----------------------------------------------------
        # Upsert vectors into Pinecone
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
        Job objects
        """

        # -----------------------------------------------------
        # Candidate → semantic text
        # -----------------------------------------------------

        resume_text = resume_to_text(
            candidate_profile
        )

        # -----------------------------------------------------
        # Candidate → embedding
        # -----------------------------------------------------

        embedding = self.embedding_tool.get_embedding(
            resume_text
        )

        if not embedding:
            return []

        # -----------------------------------------------------
        # Semantic vector search
        # -----------------------------------------------------

        matches = self.pinecone_tool.query_vectors(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
        )

        # -----------------------------------------------------
        # Convert Pinecone matches → Job objects
        # -----------------------------------------------------

        jobs: List[Job] = []

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

                # Preserve first-stage semantic score.
                #
                # This is NOT a percentage.
                # It is the similarity score returned
                # by the vector database.
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