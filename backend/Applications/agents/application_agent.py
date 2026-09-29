from backend.graphs.state import GraphState

class ApplicationAgent:
    """
    Prepares an application package for human review.
    Responsibilities:
    - Read the candidate profile from the active resume
    - Read the job selected by the user
    - Build the application context
    - Move the workflow to human approval
    This agent does NOT:
    - Submit applications
    - Interact with external websites
    - Call MCP tools
    - Update MongoDB
    - Decide whether the application is approved
    """

    def run(self,state: GraphState) -> GraphState:
            
         # 1. Get candidate profile
            candidate_profile = state.get("candidate_profile")

            if candidate_profile is None:
                raise ValueError("Candidate profile not found.")

        # 2. Get selected job
            selected_job = state.get("selected_job")
            if selected_job is None:
                raise ValueError("No job selected for application.")

        # 3. Prepare application context
            state["application_materials"] = {
            "candidate_profile": (
                candidate_profile.model_dump(
                    mode="json"
                )

            ),

            "job": (
                selected_job.model_dump(
                    mode="json"

                )
            ),

        }

            # 4. Set Initial Application State
            state["application_status"] = ("awaiting_approval")
            state["human_approval"] = None
            state["application_result"] = None
            return state

    


    
