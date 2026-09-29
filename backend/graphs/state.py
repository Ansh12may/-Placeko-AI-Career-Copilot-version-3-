#state is shared memory of langGraph workflow
from typing import Annotated, Optional
from typing_extensions import TypedDict
from backend.Resume.schemas.candidate import CandidateProfile
from backend.ATS.schemas.ats_report import ATSReport
from backend.Jobs.schemas.job import Job
from langchain_core.messages import AnyMessage
from backend.Interview.schemas.interview_session import (InterviewSession)
from backend.Interview.schemas.interview_plan import (InterviewPlan)
from backend.Interview.schemas.interview_question import (InterviewQuestion,QuestionCategory)
import operator


class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.

    Each agent reads from this state, updates it,
    and passes it to the next node in the workflow.
    """

    # Conversation History

    messages: Annotated[
        list[AnyMessage],
        operator.add,
    ]

    # Resume Information

    resume_path: Optional[str]
    resume_text: Optional[str]

    # Structured candidate profile.
    # Output of ResumeAgent.
    candidate_profile: Optional[CandidateProfile]
    grounding_result: Optional[dict]

    
    # Job Recommendation

    # Raw/discovered jobs
    jobs: Optional[list[Job]]

    # Jobs produced by the older/general ranking pipeline
    retrieved_jobs: Optional[list[Job]]
    ranked_jobs: Optional[list[Job]]
    # recommended_jobs: Optional[list[Job]]

    # Job selected by the user
    selected_job: Optional[Job]


    
    # Interview
    interview_session: Optional[InterviewSession]
    interview_plan: Optional[InterviewPlan]
    current_question: Optional[str]
    question_number: Optional[int]
    current_category: Optional[str]
    previous_questions: Optional[list[str]]

   
    # Workflow Metadata

    next_node: Optional[str]

   
    # Error Information
    
    error: Optional[str]

    # ATS Analysis

    ats_report: Optional[ATSReport]

    # Application Workflow
    application_id: Optional[str]
    application_status: Optional[str]
    application_materials: Optional[dict]
    human_approval: Optional[bool]
    application_result: Optional[dict]
    application_thread_id: Optional[str]

    workflow_type: Optional[str]