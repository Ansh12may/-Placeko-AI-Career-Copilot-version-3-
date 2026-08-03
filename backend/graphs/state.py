#state is shared memory of langGraph workflow
from typing import Annotated, Optional
from typing_extensions import TypedDict
from backend.schemas.candidate import CandidateProfile
from backend.schemas.job import Job
from langchain_core.messages import AnyMessage
import operator

class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    Each agent reads from this state, updates it,
    and passes it to the next node in the workflow.
    """
    # Conversation history
    messages: Annotated[list[AnyMessage], operator.add]
    # Resume information
    resume_path: Optional[str]
    resume_text: Optional[str]
    # Structured candidate profile
    candidate_profile: Optional[CandidateProfile]
    #for job agents
    jobs: Optional[list[Job]]
    ranked_jobs: Optional[list[Job]]
    # Workflow metadata
    next_node: Optional[str]
    # Error information
    error: Optional[str]
    