"""
Recommendation Agent

Responsible for orchestrating first-stage semantic
job retrieval.

Production Pipeline:

CandidateProfile
        ↓
VectorService
        ↓
Candidate Embedding
        ↓
Pinecone Semantic Search
        ↓
Top 20 Retrieved Jobs
        ↓
GraphState.retrieved_jobs

This agent performs NO:
- LLM reasoning
- Embedding generation
- Pinecone operations
- CrossEncoder scoring
- Sorting logic

Those responsibilities belong to the respective
services/tools.
"""

from backend.graphs.state import GraphState
from backend.Jobs.services.vector_service import VectorService


class RecommendationAgent:

    def __init__(self):
        self.vector_service = VectorService()

    def run(self, state: GraphState) -> GraphState:
        """
        Retrieve the top 20 semantically similar jobs
        for the grounded candidate profile.
        """

        # 1. Get candidate profile

        profile = state.get("candidate_profile")

        if profile is None:
            raise ValueError(
                "Candidate profile not found."
            )

        # 2. Retrieve top 20 jobs from Pinecone

        retrieved_jobs = (
            self.vector_service.search_by_candidate(
                candidate_profile=profile,
                top_k=20,
            )
        )

        # 3. Store retrieved jobs in GraphState

        state["retrieved_jobs"] = retrieved_jobs

        return state