"""
Resume Service

Responsible for:
- Resume upload and analysis
- Resume retrieval
- Resume activation
- Resume deletion
- Coordinating ResumeAgent and ResumeAnalysisAgent

This service performs orchestration only.
It does NOT perform:
- Direct MongoDB operations
- ATS scoring logic
- LLM reasoning
- Resume parsing logic
"""

import os
import tempfile
from datetime import datetime, timezone

from fastapi import UploadFile

from backend.Resume.repositories.resume_repository import (
    ResumeRepository,
)
from backend.Resume.agents.resume_agent import ResumeAgent
from backend.ATS.agents.resume_analysis_agent import (
    ResumeAnalysisAgent,
)
from backend.graphs.state import GraphState


class ResumeService:

    def __init__(self):
        self.repository = ResumeRepository()

        self.resume_agent = ResumeAgent()

        self.resume_analysis_agent = (
            ResumeAnalysisAgent()
        )

    # =========================================================
    # Upload Resume
    # =========================================================

    async def upload_resume(
        self,
        user_id: str,
        file: UploadFile,
    ):
        """
        Upload and analyze a resume.

        Flow:

        UploadFile
            ↓
        Validate file
            ↓
        Save temporary file
            ↓
        ResumeAgent
            ↓
        CandidateProfile
            ↓
        ResumeAnalysisAgent
            ↓
        ATSReport
            ↓
        Validate analysis
            ↓
        Deactivate old resume
            ↓
        Store new resume in MongoDB
        """

        # -----------------------------------------------------
        # 1. Validate file
        # -----------------------------------------------------

        if not file.filename:
            raise ValueError(
                "Resume file name is required."
            )

        if file.content_type != "application/pdf":
            raise ValueError(
                "Only PDF resumes are supported."
            )

        # -----------------------------------------------------
        # 2. Read uploaded file
        # -----------------------------------------------------

        file_bytes = await file.read()

        if not file_bytes:
            raise ValueError(
                "Uploaded resume is empty."
            )

        # -----------------------------------------------------
        # 3. Create temporary file
        # -----------------------------------------------------

        suffix = (
            os.path.splitext(file.filename)[1]
            or ".pdf"
        )

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as temp_file:

                temp_file.write(file_bytes)

                temp_path = temp_file.name

            # -------------------------------------------------
            # 4. Prepare GraphState
            #
            # IMPORTANT:
            # We do NOT deactivate the old resume here.
            #
            # The old resume should remain active if the new
            # resume fails during analysis.
            # -------------------------------------------------

            state: GraphState = {
                "messages": [],

                "resume_path": temp_path,

                "resume_text": None,

                "candidate_profile": None,

                "jobs": None,

                "ranked_jobs": None,

                "recommended_jobs": None,

                "selected_job": None,

                "interview_session": None,

                "next_node": None,

                "error": None,

                "ats_report": None,
            }

            # -------------------------------------------------
            # 5. Run Resume Agent
            # -------------------------------------------------

            state = self.resume_agent.run(
                state
            )

            # -------------------------------------------------
            # 6. Run ATS Analysis Agent
            # -------------------------------------------------

            state = (
                self.resume_analysis_agent.run(
                    state
                )
            )

            # -------------------------------------------------
            # 7. Validate analysis results
            # -------------------------------------------------

            candidate_profile = state.get(
                "candidate_profile"
            )

            ats_report = state.get(
                "ats_report"
            )

            if candidate_profile is None:
                raise ValueError(
                    "Resume analysis failed: "
                    "candidate profile was not generated."
                )

            if ats_report is None:
                raise ValueError(
                    "Resume analysis failed: "
                    "ATS report was not generated."
                )

            # -------------------------------------------------
            # 8. Deactivate existing resumes
            #
            # IMPORTANT:
            # This happens ONLY after successful analysis.
            # -------------------------------------------------

            await self.repository.deactivate_all_resumes(
                user_id
            )

            # -------------------------------------------------
            # 9. Store new resume in MongoDB
            # -------------------------------------------------

            now = datetime.now(
                timezone.utc
            )

            resume_data = {
                "user_id": user_id,

                "file_name": file.filename,

                "file_size": len(file_bytes),

                "content_type": file.content_type,

                "candidate_profile":
                    candidate_profile.model_dump(
                        mode="json"
                    ),

                "ats_report":
                    ats_report.model_dump(
                        mode="json"
                    ),

                "ats_score":
                    ats_report.overall_score,

                "is_active": True,

                "created_at": now,

                "updated_at": now,
            }

            resume_id = (
                await self.repository.create_resume(
                    resume_data
                )
            )

            # -------------------------------------------------
            # 10. Return API response
            # -------------------------------------------------

            return {
                "success": True,

                "message":
                    "Resume uploaded and analyzed successfully.",

                "data": {
                    "resume_id": resume_id,

                    "file_name":
                        file.filename,

                    "candidate_profile":
                        candidate_profile,

                    "ats_report":
                        ats_report,

                    "is_active": True,
                },
            }

        finally:

            # -------------------------------------------------
            # 11. Remove temporary file
            # -------------------------------------------------

            if (
                temp_path
                and os.path.exists(temp_path)
            ):
                os.remove(temp_path)

    # =========================================================
    # Get User Resumes
    # =========================================================

    async def get_user_resumes(
        self,
        user_id: str,
    ):
        """
        Return all resumes belonging to the user.
        """

        resumes = (
            await self.repository.get_user_resumes(
                user_id
            )
        )

        return {
            "success": True,
            "data": resumes,
        }

    # =========================================================
    # Get Single Resume
    # =========================================================

    async def get_resume(
        self,
        user_id: str,
        resume_id: str,
    ):
        """
        Return a specific resume belonging
        to the authenticated user.
        """

        resume = (
            await self.repository.get_resume_by_id(
                resume_id=resume_id,
                user_id=user_id,
            )
        )

        if not resume:
            raise ValueError(
                "Resume not found."
            )

        return {
            "success": True,
            "data": resume,
        }

    # =========================================================
    # Set Active Resume
    # =========================================================

    async def set_active_resume(
        self,
        user_id: str,
        resume_id: str,
    ):
        """
        Set one resume as the user's active resume.
        """

        # -----------------------------------------------------
        # 1. Verify ownership
        # -----------------------------------------------------

        resume = (
            await self.repository.get_resume_by_id(
                resume_id=resume_id,
                user_id=user_id,
            )
        )

        if not resume:
            raise ValueError(
                "Resume not found."
            )

        # -----------------------------------------------------
        # 2. Deactivate all resumes
        # -----------------------------------------------------

        await self.repository.deactivate_all_resumes(
            user_id
        )

        # -----------------------------------------------------
        # 3. Activate selected resume
        # -----------------------------------------------------

        await self.repository.update_resume(
            resume_id=resume_id,
            user_id=user_id,
            update_data={
                "is_active": True,
                "updated_at":
                    datetime.now(
                        timezone.utc
                    ),
            },
        )

        return {
            "success": True,
            "message":
                "Resume activated successfully.",
        }

    # =========================================================
    # Delete Resume
    # =========================================================

    async def delete_resume(
        self,
        user_id: str,
        resume_id: str,
    ):
        """
        Delete a user's resume.
        """

        # -----------------------------------------------------
        # 1. Verify ownership
        # -----------------------------------------------------

        resume = (
            await self.repository.get_resume_by_id(
                resume_id=resume_id,
                user_id=user_id,
            )
        )

        if not resume:
            raise ValueError(
                "Resume not found."
            )

        # -----------------------------------------------------
        # 2. Delete resume
        # -----------------------------------------------------

        result = (
            await self.repository.delete_resume(
                resume_id=resume_id,
                user_id=user_id,
            )
        )

        if result.deleted_count == 0:
            raise ValueError(
                "Resume could not be deleted."
            )

        return {
            "success": True,
            "message":
                "Resume deleted successfully.",
        }