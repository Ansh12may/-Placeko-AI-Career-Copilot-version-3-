"""

Vector Service

Responsible for:

1. Converting Job objects into searchable text.

2. Generating job embeddings.

3. Storing job vectors in Pinecone.

4. Generating a candidate embedding.

5. Retrieving semantically similar jobs from Pinecone.

6. Converting Pinecone results back into Job objects.

Production pipeline:

JobSearchAgent

        ↓

Fresh Jobs

        ↓

store_jobs()

        ↓

EmbeddingTool

        ↓

Pinecone

JobRetrievalAgent

        ↓

CandidateProfile

        ↓

search_by_candidate(top_k=20)

        ↓

EmbeddingTool

        ↓

Pinecone

        ↓

20 Retrieved Jobs

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

    Service responsible for:

    - Job vector creation and storage.

    - First-stage semantic job retrieval.

    """

    def __init__(self):

        self.embedding_tool = EmbeddingTool()

        self.pinecone_tool = PineconeTool()

    # =========================================================

    # Store Jobs

    # =========================================================

    def store_jobs(self, jobs: List[Job]) -> None:

        """

        Convert fresh jobs into embeddings and store them

        in Pinecone.

        Flow:

        Jobs

          ↓

        job_to_text()

          ↓

        Embeddings

          ↓

        Pinecone upsert

        """

        if not jobs:

            return

        # 1. Convert jobs into searchable text

        job_texts = [

            job_to_text(job)

            for job in jobs

        ]

        # 2. Generate embeddings in batch

        embeddings = (

            self.embedding_tool

            .get_embeddings(job_texts)

        )

        if not embeddings:

            return

        # 3. Build Pinecone vectors

        vectors = []

        for job, embedding in zip(

            jobs,

            embeddings,

        ):

            if not embedding:

                continue

            # Prefer application URL as the stable

            # identity of the job posting.

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

        # 4. Upsert vectors into Pinecone

        if vectors:

            self.pinecone_tool.upsert_vectors(

                vectors

            )

    # =========================================================

    # Semantic Retrieval

    # =========================================================

    def search_by_candidate(

        self,

        candidate_profile: CandidateProfile,

        top_k: int = 20,

    ) -> List[Job]:

        """

        Retrieve semantically similar jobs for a candidate.

        This is the first-stage retrieval step.

        Production flow:

        CandidateProfile

              ↓

        resume_to_text()

              ↓

        EmbeddingTool

              ↓

        Candidate Embedding

              ↓

        Pinecone

              ↓

        Top 20 Matches

              ↓

        Job objects

        CrossEncoder reranking is NOT performed here.

        """

        if candidate_profile is None:

            raise ValueError(

                "Candidate profile is required."

            )

        # 1. Convert candidate profile into

        #    semantic search text.

        candidate_text = resume_to_text(

            candidate_profile

        )

        if not candidate_text.strip():

            return []

        # 2. Generate candidate embedding.

        embedding = (

            self.embedding_tool

            .get_embedding(candidate_text)

        )

        if not embedding:

            return []

        # 3. Retrieve semantically similar jobs

        #    from Pinecone.

        matches = (

            self.pinecone_tool.query_vectors(

                vector=embedding,

                top_k=top_k,

                include_metadata=True,

            )

        )

        # 4. Convert Pinecone results into

        #    validated Job objects.

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

                # 5. Deduplicate jobs.

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

                # 6. Preserve Pinecone similarity

                #    score for downstream use/debugging.

                if hasattr(match, "score"):

                    job.pinecone_score = float(match.score)

                jobs.append(job)

            except Exception:

                # Ignore malformed Pinecone metadata

                # without failing the entire retrieval.

                continue

        return jobs