from datetime import datetime
from backend.graphs.state import GraphState


class ApplicationExecutorAgent:
    """
    Executes an approved job application.

    Responsibilities:
    - Verify that the application was approved
    - Read the prepared application package
    - Execute the submission through the configured
      application execution layer
    - Store the submission result in GraphState

    This agent does NOT:
    - Decide whether an application should be submitted
    - Ask the user for approval
    - Search for jobs
    - Perform job recommendation
    """

    def run(self,state: GraphState) -> GraphState:

        # 1. Verify Human Approval
        if state.get("human_approval") is not True:
            raise ValueError(
                "Application has not been approved."
            )

        # 2. Get Application Materials
        
        application_materials = state.get(
            "application_materials"
        )

        if not application_materials:
            raise ValueError(
                "Application materials not found."
            )

        # =====================================================
        # 3. Execute Application
        # =====================================================

        #
        # IMPORTANT:
        # The actual external submission mechanism will be
        # connected here later.
        #
        # For now this is the execution boundary.
        #

        result = self._execute_application(
            application_materials
        )

      
        # 4. Store Result
     
        state["application_result"] = result

        if result.get("success"):

            state["application_status"] = (
                "submitted"
            )

        else:

            state["application_status"] = (
                "submission_failed"
            )

        return state

    # EXECUTION BOUNDARY
  
    def _execute_application(self,application_materials: dict,) -> dict:
        """
        Execute the actual job application.

        This method is intentionally isolated from the
        LangGraph orchestration layer.

        Later this can delegate to:
            MCP client
                ↓
            browser/application tool
                ↓
            external job platform

        without changing the GraphState contract.
        """

        job = application_materials.get(
            "job"
        )

        candidate_profile = application_materials.get(
            "candidate_profile"
        )

        if not job:
            raise ValueError(
                "Job information missing."
            )

        if not candidate_profile:
            raise ValueError(
                "Candidate profile missing."
            )

        # -----------------------------------------------------
        # TEMPORARY EXECUTION RESULT
        # -----------------------------------------------------
        #
        # DO NOT claim that the application was actually
        # submitted yet.
        #
        # This is only a placeholder until the external
        # execution layer is implemented.
        #

        return {
            "success": False,
            "status": "executor_not_configured",
            "message": (
                "Application execution layer "
                "has not been configured yet."
            ),
            "job_id": job.get("job_id"),
            "timestamp": datetime.utcnow().isoformat(),
        }