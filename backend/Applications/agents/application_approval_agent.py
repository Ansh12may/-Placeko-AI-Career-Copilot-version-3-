from langgraph.types import interrupt
from backend.graphs.state import GraphState

class ApplicationApprovalAgent:
    """
    Human-in-the-loop approval node.
    Responsibilities:
    - Present the prepared application to the user
    - Pause the LangGraph workflow
    - Receive an explicit approval/rejection decision
    - Store the decision in GraphState

    This agent does NOT:
    - Submit applications
    - Call external job sites
    - Use MCP tools
    - Update the application tracker
    """

    def run(self,state: GraphState) -> GraphState:

        # Application must be prepared first
        application_materials = state.get("application_materials")

        if not application_materials:
            raise ValueError(
                "Application materials not found."
            )

       
        # Pause workflow for human decision
        
        decision = interrupt(
            {
                "type": "application_approval",
                "message": (
                    "Review the prepared application "
                    "before submission."
                ),
                "application": application_materials,
            }
        )

        # Validate decision

        if not isinstance(decision, dict):
            raise ValueError(
                "Invalid application approval response."
            )

        approved = decision.get(
            "approved"
        )

        if not isinstance(approved, bool):
            raise ValueError(
                "Application approval must be "
                "a boolean value."
            )

        # Update workflow state
      
        state["human_approval"] = approved

        if approved:
            state["application_status"] = ("approved")
        else:
            state["application_status"] = ("rejected")

        return state