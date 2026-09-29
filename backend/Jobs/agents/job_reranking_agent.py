"""
Job Reranking Agent
Responsible for the second-stage job ranking pipeline.
Production Pipeline:
Retrieved Jobs (Top 20)
        ↓
CandidateProfile
        ↓
CrossEncoder
        ↓
Reranked Jobs
        ↓
Top 10
        ↓
ranked_jobs

This agent performs orchestration only.

It does NOT:
- Generate embeddings
- Query Pinecone
- Perform CrossEncoder inference directly
- Sort jobs directly
- Perform LLM reasoning

Those responsibilities belong to the respective
services/tools.
"""

from backend.graphs.state import GraphState
from backend.Jobs.services.reranker_service import RerankerService


class JobRerankingAgent:

    def __init__(self):
        self.reranker_service = RerankerService()

    def run(self, state: GraphState) -> GraphState:
        """
        Rerank the semantically retrieved jobs using
        the CrossEncoder and keep the top 10.
        """

        # 1. Get candidate profile

        profile = state.get("candidate_profile")

        if profile is None:
            raise ValueError(
                "Candidate profile not found."
            )

        # 2. Get Pinecone retrieved jobs

        retrieved_jobs = state.get(
            "retrieved_jobs",
            [],
        )

        if not retrieved_jobs:
            state["ranked_jobs"] = []
            return state

        # 3. CrossEncoder reranking

        ranked_jobs = (
        self.reranker_service.rerank(
            candidate_profile=profile,
            jobs=retrieved_jobs,
            top_k=10,
        )
    )
        state["ranked_jobs"] = ranked_jobs

        return state