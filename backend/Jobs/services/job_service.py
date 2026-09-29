"""
Job Service

Responsible for:
- Fetching the authenticated user's active resume
- Loading the stored CandidateProfile
- Checking persisted job recommendations
- Preparing the initial GraphState
- Executing the job recommendation graph when needed
- Persisting final ranked recommendations

This service performs orchestration only.
"""

from typing import List
import asyncio

from backend.Jobs.schemas.job import Job
from backend.Jobs.repositories.job_repository import JobRepository
from backend.Resume.repositories.resume_repository import ResumeRepository
from backend.Resume.schemas.candidate import CandidateProfile
from backend.graphs.state import GraphState
from backend.graphs.workflow import builder
from backend.Jobs.services.job_readiness_service import JobReadinessService


class JobService:

    def __init__(self):
        self.resume_repository = ResumeRepository()
        self.job_repository = JobRepository()
        self.graph = builder.compile()
        self.readiness_service = JobReadinessService()

    
    # GET RECOMMENDED JOBS
 

    async def get_recommended_jobs(
        self,
        current_user,
    ) -> List[Job]:
        """
        Return personalized job recommendations.

        Persistence flow:

        First request:

            User
              ↓
            Active Resume
              ↓
            MongoDB lookup
              ↓
            No recommendations
              ↓
            Recommendation Graph
              ↓
            JSearch
              ↓
            Pinecone
              ↓
            Semantic Retrieval
              ↓
            CrossEncoder
              ↓
            ranked_jobs
              ↓
            MongoDB
              ↓
            Return ranked_jobs

        Subsequent request:

            User
              ↓
            Active Resume
              ↓
            MongoDB lookup
              ↓
            Persisted ranked_jobs
              ↓
            Return ranked_jobs
        """

        # 1. Get authenticated user's ID
        

        user_id = str(
            current_user["_id"]
        )

        
        # 2. Get user's active resume
      

        resume = await self.resume_repository.get_active_resume(
            user_id=user_id
        )

        if not resume:
            raise ValueError(
                "No active resume found. "
                "Please upload a resume first."
            )

        resume_id = resume["id"]

        
        # 3. Check persisted recommendations
        

        persisted_jobs = (
            await self.job_repository.get_recommendations(
                user_id=user_id,
                resume_id=resume_id,
            )
        )

        grounded_profile_data = resume.get("grounded_candidate_profile")
        profile_data = grounded_profile_data or resume.get("candidate_profile")

        if persisted_jobs:
            return await self.readiness_service.analyze_jobs(
                profile=CandidateProfile.model_validate(profile_data or {}),
                jobs=persisted_jobs,
                user_id=user_id,
                resume_id=resume_id,
            )

        
        # 4. Get stored CandidateProfile
        

        candidate_profile_data = resume.get(
            "candidate_profile"
        )

        if not candidate_profile_data:
            raise ValueError(
                "Candidate profile not found "
                "for active resume."
            )

        # 5. Validate CandidateProfile
       

        candidate_profile = CandidateProfile.model_validate(
            grounded_profile_data or candidate_profile_data
        )

       
        # 6. Prepare GraphState
       

        initial_state: GraphState = {

            "messages": [],

            # Resume information
            "resume_path": None,
            "resume_text": None,

            # Candidate information
            "candidate_profile": candidate_profile,
            "grounding_result": None,

            # Job recommendation pipeline
            "jobs": None,
            "retrieved_jobs": None,
            "ranked_jobs": None,

            # User-selected job
            "selected_job": None,

            # Interview
            "interview_session": None,

            # Workflow metadata
            "next_node": None,

            # Error
            "error": None,

            # ATS
            "ats_report": None,

            # Application workflow
            "application_id": None,
            "application_status": None,
            "application_materials": None,
            "human_approval": None,
            "application_result": None,
            "application_thread_id": None,

            # Current workflow
            "workflow_type": "recommendation",
        }

       
        # 7. Execute recommendation graph
       

        result = await asyncio.to_thread(
            self.graph.invoke,
            initial_state,
        )

        
        # 8. Get final ranked recommendations
        

        ranked_jobs = result.get(
            "ranked_jobs",
            [],
        )

    
        # 9. Build requirement-to-evidence readiness data
        

        ranked_jobs = await self.readiness_service.analyze_jobs(
            profile=candidate_profile,
            jobs=ranked_jobs,
            user_id=user_id,
            resume_id=resume_id,
        )

        
        # 10. Persist FINAL ranked recommendations
        

        if ranked_jobs:

            await self.job_repository.save_recommendations(
                user_id=user_id,
                resume_id=resume_id,
                jobs=ranked_jobs,
            )

        
        # 10. Return final ranked recommendations
        

        return ranked_jobs

 

    # GET SINGLE JOB DETAILS

   
    async def get_job_details(

        self,

        user_id: str,

        resume_id: str,

        job_id: str,

    ) -> Job:

        """

        Retrieve a single persisted job recommendation.

        This method performs no job searching or ranking.

        It only retrieves a job that already exists in the

        user's persisted recommendation snapshot.

        """

        job = await self.job_repository.get_job(

            user_id=user_id,

            resume_id=resume_id,

            job_id=job_id,

        )

        if not job:

            raise ValueError(

                "Job not found in the user's recommendations."

            )

        return job

    async def confirm_job_requirement(
        self,
        current_user,
        job: Job,
        requirement: str,
    ) -> None:
        """Persist an explicit candidate confirmation for a job requirement."""

        user_id = str(current_user["_id"])
        resume = await self.resume_repository.get_active_resume(user_id=user_id)

        if not resume:
            raise ValueError("No active resume found. Please upload a resume first.")

        await self.readiness_service.confirm_requirement(
            user_id=user_id,
            resume_id=resume["id"],
            job=job,
            requirement=requirement,
        )
