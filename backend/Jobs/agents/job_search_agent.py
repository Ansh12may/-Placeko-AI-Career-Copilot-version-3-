from backend.utils.base_agent import BaseAgent
from backend.graphs.state import GraphState
from backend.Jobs.prompts.job_search_prompt import JOB_SEARCH_PROMPT
from backend.Jobs.tools.job_search_tool import JobSearchTool
from backend.Jobs.services.vector_service import VectorService
from backend.config.settings import settings


class JobSearchAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        self.llm = settings.llm
        self.system_prompt = JOB_SEARCH_PROMPT

        self.job_tool = JobSearchTool()

        # Handles job embeddings and Pinecone indexing.
        self.vector_service = VectorService()

    def prepare_input(
        self,
        state: GraphState,
    ) -> str:

        profile = state.get("candidate_profile")

        if profile is None:
            raise ValueError(
                "Candidate profile not found."
            )

        return profile.model_dump_json(
            indent=2
        )

    def generate_query(
        self,
        candidate_json: str,
    ) -> str:

        messages = [
            (
                "system",
                self.system_prompt,
            ),
            (
                "human",
                candidate_json,
            ),
        ]

        response = self.llm.invoke(messages)

        query = response.content.strip()

        if not query:
            raise ValueError(
                "LLM returned an empty job search query."
            )

        return query

    def invoke_tool(
        self,
        query: str,
    ):

        return self.job_tool.search_jobs(
            query
        )

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        # =====================================================
        # 1. CandidateProfile → JSON
        # =====================================================

        candidate_json = self.prepare_input(
            state
        )

        # =====================================================
        # 2. LLM → Job Search Query
        # =====================================================

        query = self.generate_query(
            candidate_json
        )

        # =====================================================
        # 3. JSearch → Fresh Jobs
        # =====================================================

        jobs = self.invoke_tool(
            query
        )

        # =====================================================
        # 4. Store Fresh Jobs in GraphState
        # =====================================================

        state["jobs"] = jobs

        # =====================================================
        # 5. Index Fresh Jobs in Pinecone
        # =====================================================

        if jobs:
            self.vector_service.store_jobs(
                jobs
            )

        return state