"""
Job Search Agent

Responsible for:

1. Reading the grounded CandidateProfile from GraphState.
2. Generating a job-search query using the LLM.
3. Fetching fresh jobs from JSearch.
4. Storing fresh jobs in GraphState.
5. Indexing fresh jobs into Pinecone.

Production Pipeline:

Grounded CandidateProfile
        ↓
JobSearchAgent
        ↓
LLM → Search Query
        ↓
JSearch
        ↓
Fresh Jobs
        ↓
VectorService.store_jobs()
        ↓
Pinecone

This agent does NOT:
- Generate embeddings directly
- Query Pinecone
- Perform semantic retrieval
- Perform CrossEncoder reranking
- Rank jobs
"""

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
        self.vector_service = VectorService()

    # =========================================================
    # Prepare Input
    # =========================================================

    def prepare_input(
        self,
        state: GraphState,
    ) -> str:
        """
        Read the grounded CandidateProfile from GraphState
        and convert it to JSON for query generation.
        """

        profile = state.get("candidate_profile")

        if profile is None:
            raise ValueError(
                "Candidate profile not found."
            )

        return profile.model_dump_json(
            indent=2
        )

    # =========================================================
    # Generate Search Query
    # =========================================================

    def generate_query(
        self,
        candidate_json: str,
    ) -> str:
        """
        Generate a concise job-search query from the
        CandidateProfile using the LLM.
        """

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

    # =========================================================
    # Search Jobs
    # =========================================================

    def invoke_tool(
        self,
        query: str,
    ):
        """
        Fetch fresh jobs from JSearch.
        """

        return self.job_tool.search_jobs(
            query
        )

    # =========================================================
    # Run Agent
    # =========================================================

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute the job search stage.

        Flow:

        CandidateProfile
              ↓
        LLM Query Generation
              ↓
        JSearch
              ↓
        Fresh Jobs
              ↓
        Pinecone Indexing
        """

        # 1. CandidateProfile → JSON

        candidate_json = self.prepare_input(
            state
        )

        # 2. CandidateProfile → Search Query

        query = self.generate_query(
            candidate_json
        )

        # 3. Search JSearch for fresh jobs

        jobs = self.invoke_tool(
            query
        )

        # 4. Store fresh jobs in GraphState

        state["jobs"] = jobs

        # 5. Index fresh jobs in Pinecone

        if jobs:
            self.vector_service.store_jobs(
                jobs
            )

        return state