"""
Recommendation Agent

Responsible for orchestrating the semantic job
recommendation pipeline.

Pipeline:

CandidateProfile
        ↓
Semantic Retrieval
        ↓
Pinecone
        ↓
Top-N Jobs
        ↓
CrossEncoder Reranking
        ↓
Top-K Recommended Jobs

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

from backend.Jobs.services.reranker_service import (
    RerankerService,
)


class RecommendationAgent:

    def __init__(self):

        self.vector_service = (
            VectorService()
        )

        self.reranker_service = (
            RerankerService()
        )

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute the semantic recommendation pipeline.

        Flow:

        GraphState
            ↓
        CandidateProfile
            ↓
        VectorService
            ↓
        Semantic Retrieval
            ↓
        Top-N Jobs
            ↓
        RerankerService
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

        retrieved_jobs = (
            self.vector_service.search_by_candidate(
                candidate_profile=profile,
                top_k=20,
            )
        )

        # =====================================================
        # 3. CrossEncoder Reranking
        # =====================================================

        reranked_jobs = (
            self.reranker_service.rerank(
                candidate_profile=profile,
                jobs=retrieved_jobs,
                top_k=5,
            )
        )

        # =====================================================
        # 4. Update GraphState
        # =====================================================

        state["ranked_jobs"] = reranked_jobs

        return state