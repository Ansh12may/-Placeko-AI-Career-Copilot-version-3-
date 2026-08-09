"""
Job Retrieval Agent
Responsible for retrieving semantically similar jobs
from Pinecone.
Responsibilities:
- Read candidate profile from GraphState
- Invoke PineconeService
- Store retrieved jobs back into GraphState

This agent performs NO model inference directly.
"""

from backend.graphs.state import GraphState
from backend.Jobs.services.vector_service import VectorService


class JobRetrievalAgent:
    """
    Agent responsible for retrieving the most relevant
    jobs from Pinecone.
    """

    def __init__(self):
        self.pinecone_service = VectorService()

    def run(self, state: GraphState) -> GraphState:
        """
        Retrieve jobs from Pinecone and update GraphState.
        """

        # Read candidate profile
        candidate_profile = state.get("candidate_profile")

        if candidate_profile is None:
            raise ValueError("Candidate profile not found in GraphState.")

        # Retrieve jobs
        retrieved_jobs = self.pinecone_service.retrieve_jobs(
            candidate_profile=candidate_profile,
            top_k=100,
        )

        # Update GraphState
        state["jobs"] = retrieved_jobs

        return state