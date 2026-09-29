"""
Job Controller

Responsible for:
- Exposing job recommendation APIs
- Exposing MCP-powered job research API
- Authenticating the current user
- Delegating business logic to services

This controller performs NO:
- Job searching
- Vector retrieval
- CrossEncoder reranking
- MCP tool implementation
- LangGraph orchestration
"""

from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from pydantic import BaseModel, Field

from backend.auth.dependency.auth_dependency import (
    get_current_user,
)

from backend.Jobs.services.job_service import (
    JobService,
)

from backend.Jobs.services.job_research_service import (
    JobResearchService,
)

from backend.Jobs.schemas.job import (
    Job,
)


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class RequirementVerificationRequest(BaseModel):
    job: Job
    requirement: str = Field(
        min_length=1,
        max_length=120,
    )


class JobResearchRequest(BaseModel):
    """
    User request sent to the Job Research Agent.
    """

    query: str = Field(
        default=(
            "Find relevant AI/ML and backend jobs "
            "in India that match my resume."
        ),
        min_length=3,
        max_length=500,
    )


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"],
)


# ============================================================
# SERVICES
# ============================================================

job_service = JobService()

job_research_service = JobResearchService()


# ============================================================
# EXISTING RECOMMENDATION ENDPOINT
# ============================================================

@router.get("/recommended")
async def get_recommended_jobs(
    current_user=Depends(
        get_current_user
    ),
):
    """
    Return personalized job recommendations.

    Existing recommendation pipeline:

        Authenticated User
                ↓
           JobService
                ↓
          Active Resume
                ↓
        CandidateProfile
                ↓
        JobSearchAgent
                ↓
             JSearch
                ↓
            Pinecone
                ↓
       Semantic Retrieval
                ↓
       CrossEncoder Reranking
                ↓
             Top Jobs
    """

    try:

        jobs = await job_service.get_recommended_jobs(
            current_user=current_user,
        )

        return {
            "success": True,
            "data": jobs,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        print(
            "JOB RECOMMENDATION ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate job recommendations.",
        )


# ============================================================
# MCP JOB RESEARCH ENDPOINT
# ============================================================

@router.post("/research")
async def research_jobs(
    request: JobResearchRequest,
    current_user=Depends(
        get_current_user
    ),
):
    """
    Run the MCP-powered Job Research Agent.

    Flow:

        Authenticated User
                ↓
        Active Resume
                ↓
        LangGraph Agent
                ↓
           MCP Client
                ↓
        ┌───────┼────────┐
        ↓       ↓        ↓
      Jobs   Resume   Readiness
        ↓       ↓        ↓
        └───────┼────────┘
                ↓
          Final Report
    """

    try:

        result = await job_research_service.research_jobs(
            current_user=current_user,
            user_request=request.query,
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        print(
            "JOB RESEARCH ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to complete job research.",
        )


# ============================================================
# EXISTING REQUIREMENT VERIFICATION ENDPOINT
# ============================================================

@router.post("/readiness/verify")
async def verify_job_requirement(
    request: RequirementVerificationRequest,
    current_user=Depends(
        get_current_user
    ),
):
    """
    Record an explicit candidate confirmation
    for an unproven requirement.
    """

    try:

        await job_service.confirm_job_requirement(
            current_user=current_user,
            job=request.job,
            requirement=request.requirement,
        )

        return {
            "success": True
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        print(
            "JOB READINESS VERIFICATION ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save requirement verification.",
        )