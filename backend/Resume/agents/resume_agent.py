"""
Resume Agent

Responsible for:
- Reading the resume path from GraphState
- Parsing the resume
- Invoking the LLM for structured extraction
- Validating the CandidateProfile
- Updating GraphState

This agent performs resume understanding only.
It does NOT:
- Store resumes in MongoDB
- Calculate ATS scores
- Search for jobs
- Perform job ranking
"""

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from backend.utils.base_agent import BaseAgent
from backend.graphs.state import GraphState
from backend.config.settings import settings

from backend.Resume.prompts.resume_prompt import (
    RESUME_SYSTEM_PROMPT,
)

from backend.Resume.schemas.candidate import (
    CandidateProfile,
)

from backend.Resume.tools.resume_parser import (
    parse_resume,
)


class ResumeAgent(BaseAgent):
    """
    AI Agent responsible for understanding
    a candidate's resume.

    Workflow:

        GraphState
            ↓
        Resume Path
            ↓
        Parse Resume
            ↓
        Extract Resume Text
            ↓
        Invoke LLM
            ↓
        CandidateProfile
            ↓
        Update GraphState
    """

    def __init__(self):
        super().__init__()

        self.llm = settings.llm

        self.system_prompt = (
            RESUME_SYSTEM_PROMPT
        )

    # =========================================================
    # Prepare Input
    # =========================================================

    def prepare_input(
        self,
        state: GraphState,
    ) -> str:
        """
        Extract resume path from GraphState.
        """

        resume_path = state.get(
            "resume_path"
        )

        if not resume_path:
            raise ValueError(
                "Resume path not found in GraphState."
            )

        return resume_path

    # =========================================================
    # Resume Parser
    # =========================================================

    def invoke_tools(
        self,
        resume_path: str,
    ) -> str:
        """
        Parse the resume and extract text.
        """

        resume_text = parse_resume(
            resume_path
        )

        if not resume_text:
            raise ValueError(
                "Could not extract text from resume."
            )

        return resume_text

    # =========================================================
    # LLM Extraction
    # =========================================================

    def invoke_llm(
        self,
        resume_text: str,
    ) -> CandidateProfile:
        """
        Extract structured candidate information
        from resume text.
        """

        messages = [
            SystemMessage(
                content=self.system_prompt
            ),
            HumanMessage(
                content=resume_text
            ),
        ]

        structured_llm = (
            self.llm.with_structured_output(
                CandidateProfile
            )
        )

        candidate = structured_llm.invoke(
            messages
        )

        return candidate

    # =========================================================
    # Validation
    # =========================================================

    def validate(
        self,
        candidate: CandidateProfile,
    ) -> CandidateProfile:
        """
        CandidateProfile is already validated
        through Pydantic.
        """

        if candidate is None:
            raise ValueError(
                "Resume extraction returned no candidate profile."
            )

        return candidate

    # =========================================================
    # Update Graph State
    # =========================================================

    def update_state(
        self,
        state: GraphState,
        resume_text: str,
        candidate: CandidateProfile,
    ) -> GraphState:
        """
        Store parsed resume text and structured
        candidate profile in GraphState.
        """

        state["resume_text"] = resume_text

        state["candidate_profile"] = candidate

        return state

    # =========================================================
    # Run Agent
    # =========================================================

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute the complete resume analysis step.
        """

        # 1. Get resume path
        resume_path = self.prepare_input(
            state
        )

        # 2. Parse resume
        resume_text = self.invoke_tools(
            resume_path
        )

        # 3. Extract CandidateProfile
        candidate = self.invoke_llm(
            resume_text
        )

        # 4. Validate
        candidate = self.validate(
            candidate
        )

        # 5. Update state
        state = self.update_state(
            state,
            resume_text,
            candidate,
        )

        return state