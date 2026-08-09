#state is shared memory of langGraph workflow
from typing import Annotated, Optional
from typing_extensions import TypedDict
from backend.Resume.schemas.candidate import CandidateProfile
from backend.ATS.schemas.ats_report import ATSReport
from backend.Jobs.schemas.job import Job
from langchain_core.messages import AnyMessage
from backend.Interview.schemas.interview_session import (
    InterviewSession,
)
import operator


class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.

    Each agent reads from this state, updates it,
    and passes it to the next node in the workflow.
    """

    # =========================================================
    # Conversation History
    # =========================================================

    messages: Annotated[
        list[AnyMessage],
        operator.add,
    ]

    # =========================================================
    # Resume Information
    # =========================================================

    resume_path: Optional[str]

    resume_text: Optional[str]

    # Structured candidate profile.
    # Output of ResumeAgent.
    candidate_profile: Optional[CandidateProfile]

    # =========================================================
    # Job Recommendation
    # =========================================================

    # Raw/discovered jobs
    jobs: Optional[list[Job]]

    # Jobs produced by the older/general ranking pipeline
    ranked_jobs: Optional[list[Job]]

    # Final semantic job recommendations
    #
    # Pipeline:
    # CandidateProfile
    #       ↓
    # Resume → Text
    #       ↓
    # BGE Embedding
    #       ↓
    # Pinecone Semantic Search
    #       ↓
    # Top K Jobs
    #       ↓
    # CrossEncoder Reranking
    #       ↓
    # recommended_jobs
    recommended_jobs: Optional[list[Job]]

    # Job selected by the user
    selected_job: Optional[Job]

    # =========================================================
    # Interview
    # =========================================================

    interview_session: Optional[InterviewSession]

    # =========================================================
    # Workflow Metadata
    # =========================================================

    next_node: Optional[str]

    # =========================================================
    # Error Information
    # =========================================================

    error: Optional[str]

    # =========================================================
    # ATS Analysis
    # =========================================================

    ats_report: Optional[ATSReport]