"""
Job Reranking Agent
Responsible for reranking retrieved jobs using
a CrossEncoder model.
Responsibilities:
- Read candidate profile from GraphState
- Read retrieved jobs
- Convert candidate profile into text
- Invoke RerankerService
- Store reranked jobs back into GraphState
This agent performs NO model inference directly.
"""
from backend.graphs.state import GraphState
from backend.Jobs.services.reranker_service import RerankerService

class JobRerankingAgent:
   
    def __init__(self):
        self.reranker_service = RerankerService()

    def run(self, state: GraphState) -> GraphState:
        
        profile = state.get("candidate_profile")
        jobs = state.get("jobs", [])

        if profile is None:
            raise ValueError("Candidate profile not found.")
        
        if not jobs:
            return state
       
        reranked_jobs = self.reranker_service.rerank(
            candidate_profile=profile,
            jobs=jobs,
            top_k=5,
        )
        state["ranked_jobs"] = reranked_jobs
        return state

    