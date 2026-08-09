"""
Job Controller

Responsible for:
- Exposing job recommendation API endpoints
- Authenticating the current user
- Delegating recommendation logic to JobService

Contains NO:
- Job retrieval logic
- Embedding logic
- Pinecone logic
- Reranking logic
- Business logic
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from backend.auth.dependency.auth_dependency import (
    get_current_user,
)

from backend.Jobs.services.job_service import (
    JobService,
)


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"],
)

job_service = JobService()


@router.get("/recommended")
async def get_recommended_jobs(
    current_user=Depends(get_current_user),
):
    """
    Return personalized job recommendations
    for the authenticated user.

    Flow:

        Authenticated User
                ↓
           JobService
                ↓
        Active Resume
                ↓
        CandidateProfile
                ↓
      RecommendationAgent
                ↓
       Semantic Retrieval
                ↓
        CrossEncoder
                ↓
        Recommended Jobs
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

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate job recommendations.",
        )