"""
Recommendation Agent

Responsible for orchestrating the semantic job
recommendation pipeline.

Production Pipeline:

CandidateProfile
        ↓
Semantic Retrieval
        ↓
Pinecone
        ↓
Top-K Recommended Jobs

CrossEncoder reranking is implemented separately
but is not used in the current production pipeline
due to deployment memory constraints.

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

from backend.Jobs.services.vector_service import (
    VectorService,
)


class RecommendationAgent:

    def __init__(self):

        self.vector_service = (
            VectorService()
        )

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute the production semantic recommendation
        pipeline.

        Flow:

        GraphState
            ↓
        CandidateProfile
            ↓
        VectorService
            ↓
        Semantic Retrieval
            ↓
        Top-K Jobs
            ↓
        GraphState
        """

        # =====================================================
        # 1. Get Candidate Profile
        # =====================================================

        profile = state.get(
            "candidate_profile"
        )

        if profile is None:
            raise ValueError(
                "Candidate profile not found."
            )

        # =====================================================
        # 2. Semantic Retrieval
        # =====================================================

        recommended_jobs = (
            self.vector_service.search_by_candidate(
                candidate_profile=profile,
                top_k=5,
            )
        )

        # =====================================================
        # 3. Update GraphState
        # =====================================================

        state["ranked_jobs"] = recommended_jobs

        return state