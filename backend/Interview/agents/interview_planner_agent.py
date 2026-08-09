"""
Interview Planner Agent

Responsible for orchestrating interview planning.

Responsibilities:
- Read required inputs from GraphState
- Invoke InterviewPlannerService
- Store InterviewPlan back into GraphState

The agent contains NO business logic.
"""

from backend.graphs.state import GraphState

from backend.Interview.services.interview_planner_service import (
    InterviewPlannerService,
)

from backend.Interview.schemas.interview_plan import (
    InterviewMode,
    DifficultyLevel,
)


class InterviewPlannerAgent:
    """
    Orchestrates interview planning.
    """

    def __init__(self):
        self.planner_service = InterviewPlannerService()

    def prepare_input(
        self,
        state: GraphState,
    ):
        """
        Extract planner inputs from GraphState.
        """

        profile = state.get("candidate_profile")
        job = state.get("selected_job")

        interview_mode = state.get(
            "interview_mode",
            InterviewMode.MIXED,
        )

        difficulty = state.get(
            "difficulty",
            DifficultyLevel.MEDIUM,
        )

        if profile is None:
            raise ValueError(
                "Candidate profile not found in GraphState."
            )

        return (
            profile,
            job,
            interview_mode,
            difficulty,
        )

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Generate InterviewPlan and store it.
        """

        (
            profile,
            job,
            interview_mode,
            difficulty,
        ) = self.prepare_input(state)

        interview_plan = self.planner_service.generate_plan(
            profile=profile,
            job=job,
            interview_mode=interview_mode,
            difficulty=difficulty,
        )

        state["interview_plan"] = interview_plan

        return state