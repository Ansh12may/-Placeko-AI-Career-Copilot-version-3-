from backend.agents.base_agent import BaseAgent
from backend.graphs.state import GraphState
from backend.prompts.job_search_prompt import JOB_SEARCH_PROMPT
from backend.tools.job_search import JobSearchTool
from backend.config.settings import settings

class JobSearchAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = settings.llm
        self.system_prompt = JOB_SEARCH_PROMPT
        self.job_tool = JobSearchTool()

    def prepare_input(self, state: GraphState) -> str:
        """
        Prepare candidate profile for the LLM.
        """
        profile = state.get("candidate_profile")
        if profile is None:
            raise ValueError("Candidate profile not found.")
        return profile.model_dump_json(indent=2)



    def generate_query(self, candidate_json: str) -> str:
        """
        Generate job search query.
        """
        messages = [
            ("system", self.system_prompt),
            ("human", candidate_json),
        ]
        response = self.llm.invoke(messages)
        query = response.content.strip()
        if not query:
            raise ValueError("LLM returned an empty job search query.")
        return query


    def invoke_tool(self, query: str):

        """
        Fetch jobs using the search tool.
        """
        return self.job_tool.search_jobs(query)


    def run(self, state: GraphState) -> GraphState:
        """
        Execute the Job Search Agent.
        """
        candidate_json = self.prepare_input(state)
        query = self.generate_query(candidate_json)
        jobs = self.invoke_tool(query)
        state["jobs"] = jobs
        return state
    

