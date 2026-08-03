from langchain_core.messages import HumanMessage, SystemMessage
from backend.agents.base_agent import BaseAgent
from backend.graphs.state import GraphState
from backend.config.settings import settings
from backend.prompts.resume_prompt import RESUME_SYSTEM_PROMPT
from backend.schemas.candidate import CandidateProfile
from backend.tools.resume_parser import parse_resume


class ResumeAgent(BaseAgent):
    """
    AI Agent responsible for understanding a candidate's resume.
    Workflow:
        GraphState
            ↓
        Parse Resume
            ↓
        Invoke LLM
            ↓
        Validate Output
            ↓
        Update GraphState
    """
    def __init__(self):
        super().__init__()
        self.llm = settings.llm
        self.system_prompt = RESUME_SYSTEM_PROMPT

    def prepare_input(self, state: GraphState) -> str:
        """
        Extract resume path from GraphState.
        """
        resume_path = state.get("resume_path")

        if not resume_path:
            raise ValueError("Resume path not found in GraphState.")

        return resume_path

    def invoke_tools(self, resume_path: str) -> str:
        """
        Invoke resume parser tool.
        """
        return parse_resume(resume_path)

    def invoke_llm(self, resume_text: str) -> CandidateProfile:
        """
        Extract structured candidate information.
        """

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=resume_text),
        ]

        structured_llm = self.llm.with_structured_output(
            CandidateProfile
        )
        candidate = structured_llm.invoke(messages)
        return candidate

    def validate(
        self,
        candidate: CandidateProfile,
    ) -> CandidateProfile:
        """
        Pydantic already validates the schema.
        Later we can add:
        - Confidence score
        - Validation Agent
        - Source Grounding
        """

        return candidate

    def update_state(
        self,
        state: GraphState,
        resume_text: str,
        candidate: CandidateProfile,
    ) -> GraphState:

        state["resume_text"] = resume_text
        state["candidate_profile"] = candidate

        return state

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        resume_path = self.prepare_input(state)
        resume_text = self.invoke_tools(resume_path)
        candidate = self.invoke_llm(resume_text)
        candidate = self.validate(candidate)
        state = self.update_state(
            state,
            resume_text,
            candidate,
        )

        return state