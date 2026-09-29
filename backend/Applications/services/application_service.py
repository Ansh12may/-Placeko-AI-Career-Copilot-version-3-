"""
Application Service

Application service responsible for managing the complete
job application lifecycle.

Responsibilities
----------------
- Create applications
- Retrieve applications
- Update application details
- Move applications through Kanban stages
- Delete applications

This service contains application business logic.

It does NOT contain:
- FastAPI routing
- HTTP logic
- Frontend logic
- Database-specific logic
"""

from datetime import datetime
from uuid import uuid4
from typing import List
import asyncio

from backend.Applications.schemas.application import (
    Application,
    ApplicationStatus,
)

from backend.Applications.schemas.application_request import (
    ApplicationCreateRequest,
    ApplicationStatusUpdateRequest,
    ApplicationUpdateRequest,
)

from backend.Applications.repositories.application_repository import (
    ApplicationRepository,
)

from uuid import uuid4

from langgraph.types import Command

from backend.graphs.workflow import graph
from backend.graphs.state import GraphState

from backend.Resume.repositories.resume_repository import (
    ResumeRepository,
)

from backend.Resume.schemas.candidate import (
    CandidateProfile,
)


class ApplicationService:
    """
    Coordinates application tracking operations.
    """

    def __init__(self):
        self.repository = ApplicationRepository()
        self.resume_repository = ResumeRepository()

 
    # CREATE APPLICATION
    
    async def create_application(
        self,
        request: ApplicationCreateRequest,
        user_id: str,
    ) -> Application:
        """
        Create a new application for the authenticated user.
        """

        now = datetime.utcnow()

        applied_at = None

        if request.status == ApplicationStatus.APPLIED:
            applied_at = now

        application = Application(
            id=str(uuid4()),

            user_id=user_id,

            job_id=request.job_id,

            job_title=request.job_title,

            company=request.company,

            location=request.location,

            apply_url=request.apply_url,

            status=request.status,

            notes=request.notes,

            applied_at=applied_at,

            created_at=now,

            updated_at=now,
        )

        return await self.repository.create(
            application
        )

    # =========================================================
    # GET APPLICATION
    # =========================================================

    async def get_application(
        self,
        application_id: str,
        user_id: str,
    ) -> Application:
        """
        Retrieve one application belonging to the user.
        """

        application = await self.repository.get_by_id(
            application_id=application_id,
            user_id=user_id,
        )

        if not application:
            raise ValueError(
                "Application not found."
            )

        return application

    # =========================================================
    # LIST APPLICATIONS
    # =========================================================

    async def get_applications(
        self,
        user_id: str,
    ) -> List[Application]:
        """
        Retrieve all applications belonging to the user.
        """

        applications = (
            await self.repository.list_by_user(
                user_id=user_id
            )
        )

        # Newest applications first
        applications.sort(
            key=lambda application: (
                application.updated_at
            ),
            reverse=True,
        )

        return applications

    # =========================================================
    # UPDATE APPLICATION
    # =========================================================

    async def update_application(
        self,
        application_id: str,
        request: ApplicationUpdateRequest,
        user_id: str,
    ) -> Application:
        """
        Update editable application information.
        """

        application = await self.get_application(
            application_id=application_id,
            user_id=user_id,
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        # -----------------------------------------------------
        # Update fields
        # -----------------------------------------------------

        for field, value in update_data.items():

            if field == "status":
                continue

            setattr(
                application,
                field,
                value,
            )

        # -----------------------------------------------------
        # Handle status separately
        # -----------------------------------------------------

        if "status" in update_data:

            status_request = (
                ApplicationStatusUpdateRequest(
                    status=update_data["status"]
                )
            )

            application = (
                await self._change_status(
                    application=application,
                    request=status_request,
                )
            )

        application.updated_at = datetime.utcnow()

        return await self.repository.update(
            application
        )

    # =========================================================
    # UPDATE STATUS
    # =========================================================

    async def update_status(
        self,
        application_id: str,
        request: ApplicationStatusUpdateRequest,
        user_id: str,
    ) -> Application:
        """
        Move an application to another Kanban stage.
        """

        application = await self.get_application(
            application_id=application_id,
            user_id=user_id,
        )

        application = self._change_status(
            application=application,
            request=request,
        )

        application.updated_at = datetime.utcnow()

        return await self.repository.update(
            application
        )

    # =========================================================
    # STATUS BUSINESS LOGIC
    # =========================================================

    def _change_status(
        self,
        application: Application,
        request: ApplicationStatusUpdateRequest,
    ) -> Application:
        """
        Apply business rules when changing application status.
        """

        old_status = application.status

        new_status = request.status

        # -----------------------------------------------------
        # No change
        # -----------------------------------------------------

        if old_status == new_status:
            return application

        # -----------------------------------------------------
        # Applied timestamp
        # -----------------------------------------------------

        if (
            new_status == ApplicationStatus.APPLIED
            and application.applied_at is None
        ):
            application.applied_at = (
                datetime.utcnow()
            )

        # -----------------------------------------------------
        # Moving back from applied
        # -----------------------------------------------------

        if (
            new_status == ApplicationStatus.SAVED
            and old_status != ApplicationStatus.SAVED
        ):
            application.applied_at = None

        # -----------------------------------------------------
        # Update status
        # -----------------------------------------------------

        application.status = new_status

        return application

    # =========================================================
    # DELETE APPLICATION
    # =========================================================

    async def delete_application(
        self,
        application_id: str,
        user_id: str,
    ) -> None:
        """
        Delete an application belonging to the user.
        """

        application = await self.get_application(
            application_id=application_id,
            user_id=user_id,
        )

        deleted = await self.repository.delete(
            application_id=application.id,
            user_id=user_id,
        )

        if not deleted:
            raise ValueError(
                "Failed to delete application."
            )

    async def start_application_workflow(
    self,
    job,
    user_id: str,
):
        """
        Start the agentic application workflow.

        The workflow prepares the application and pauses at
        the human approval checkpoint.
        """

        # -----------------------------------------------------
        # 1. Get active resume
        # -----------------------------------------------------

        resume = (
            await self.resume_repository.get_active_resume(
                user_id=user_id
            )
        )

        if not resume:
            raise ValueError(
                "No active resume found. "
                "Please upload a resume first."
            )

        # -----------------------------------------------------
        # 2. Get candidate profile
        # -----------------------------------------------------

        candidate_profile_data = (
            resume.get("candidate_profile")
        )

        if not candidate_profile_data:
            raise ValueError(
                "Candidate profile not found "
                "for active resume."
            )

        candidate_profile = (
            CandidateProfile.model_validate(
                candidate_profile_data
            )
        )

        # -----------------------------------------------------
        # 3. Create workflow thread
        # -----------------------------------------------------

        thread_id = str(uuid4())

        # -----------------------------------------------------
        # 4. Prepare GraphState
        # -----------------------------------------------------

        initial_state: GraphState = {
            "messages": [],

            "resume_path": None,
            "resume_text": None,

            "candidate_profile": candidate_profile,

            "jobs": None,
            "ranked_jobs": None,
            "recommended_jobs": None,

            "selected_job": job,

            "interview_session": None,

            "application_id": None,
            "application_status": None,
            "application_materials": None,
            "human_approval": None,
            "application_result": None,

            "workflow_type": "application",
            "application_thread_id": thread_id,

            "next_node": None,
            "error": None,
            "ats_report": None,
        }

        # -----------------------------------------------------
        # 5. Configure LangGraph thread
        # -----------------------------------------------------

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        # -----------------------------------------------------
        # 6. Start graph
        # -----------------------------------------------------

        result = await asyncio.to_thread(
            graph.invoke,
            initial_state,
            config,
        )

        return {
            "thread_id": thread_id,
            "state": result,
        }