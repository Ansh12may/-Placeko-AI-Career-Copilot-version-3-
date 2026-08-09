"""
Job Service

Responsible for:
- Fetching the authenticated user's active resume
- Preparing the initial GraphState
- Executing the job recommendation graph
- Returning semantic job recommendations

This service performs orchestration only.

It does NOT perform:
- Embedding generation
- Pinecone search
- CrossEncoder reranking
- LLM reasoning
"""

from typing import List

from backend.Jobs.schemas.job import Job

from backend.Resume.repositories.resume_repository import (
    ResumeRepository,
)

from backend.graphs.state import GraphState

from backend.graphs.workflow import (
    builder,
)


class JobService:

    def __init__(self):
        self.resume_repository = ResumeRepository()
        self.graph = builder.compile()

    async def get_recommended_jobs(
        self,
        current_user,
    ) -> List[Job]:
        """
        Generate personalized job recommendations
        using the authenticated user's active resume.

        Flow:

        User
          ↓
        Active Resume
          ↓
        CandidateProfile
          ↓
        RecommendationAgent
          ↓
        Semantic Retrieval
          ↓
        CrossEncoder Reranking
          ↓
        ranked_jobs
        """

        # =====================================================
        # 1. Get authenticated user's ID
        # =====================================================

        user_id = str(
            current_user["_id"]
        )

        # =====================================================
        # 2. Get user's active resume
        # =====================================================

        resume = (
            await self.resume_repository
            .get_active_resume(
                user_id=user_id
            )
        )

        if not resume:
            raise ValueError(
                "No active resume found. "
                "Please upload a resume first."
            )

        # =====================================================
        # 3. Get stored CandidateProfile
        # =====================================================

        candidate_profile_data = (
            resume.get("candidate_profile")
        )

        if not candidate_profile_data:
            raise ValueError(
                "Candidate profile not found "
                "for active resume."
            )

        # =====================================================
        # 4. Convert stored data into CandidateProfile
        # =====================================================

        from backend.Resume.schemas.candidate import (
            CandidateProfile,
        )

        candidate_profile = (
            CandidateProfile.model_validate(
                candidate_profile_data
            )
        )

        # =====================================================
        # 5. Prepare GraphState
        # =====================================================

        initial_state: GraphState = {
            "messages": [],

            "resume_path": None,

            "resume_text": None,

            "candidate_profile": candidate_profile,

            "jobs": None,

            "ranked_jobs": None,

            "selected_job": None,

            "interview_session": None,

            "next_node": None,

            "error": None,

            "ats_report": None,
        }

        # =====================================================
        # 6. Execute recommendation graph
        # =====================================================

        result = self.graph.invoke(
            initial_state
        )

        # =====================================================
        # 7. Get ranked recommendations
        # =====================================================

        ranked_jobs = result.get(
            "ranked_jobs",
            [],
        )

        return ranked_jobs