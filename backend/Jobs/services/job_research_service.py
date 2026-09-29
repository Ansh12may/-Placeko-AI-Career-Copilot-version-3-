from typing import Any

from backend.Jobs.agents.job_research_agent import (
    build_research_graph,
)
from backend.Resume.repositories.resume_repository import (
    ResumeRepository,
)


class JobResearchService:
    """
    Application service for the MCP-powered Job Research Agent.

    Responsibilities:
    - Resolve the authenticated user's active resume.
    - Build the Job Research LangGraph.
    - Execute the research workflow.
    - Return the final grounded report.

    This service does NOT contain:
    - Job search logic
    - Resume grounding logic
    - MCP tool implementations
    - Recommendation logic
    """

    def __init__(self):
        self.resume_repository = ResumeRepository()

    async def research_jobs(
        self,
        current_user: dict[str, Any],
        user_request: str,
    ) -> dict[str, Any]:

        user_id = str(
            current_user["_id"]
        )

        # ----------------------------------------------------
        # ACTIVE RESUME
        # ----------------------------------------------------

        resume = await self.resume_repository.get_active_resume(
            user_id=user_id
        )

        if not resume:
            raise ValueError(
                "No active resume found. Please upload a resume first."
            )

        resume_id = str(
            resume["id"]
        )

        # ----------------------------------------------------
        # BUILD RESEARCH GRAPH
        # ----------------------------------------------------

        graph = build_research_graph()

        initial_state = {
            "user_id": user_id,
            "resume_id": resume_id,
            "user_request": user_request,
            "messages": [],
            "tool_results": [],
            "final_report": "",
            "research_rounds": 0,
        }

        # ----------------------------------------------------
        # EXECUTE AGENT
        # ----------------------------------------------------

        result = await graph.ainvoke(
            initial_state,
            {
                "recursion_limit": 10,
            },
        )

        # ----------------------------------------------------
        # EXTRACT TOOL USAGE
        # ----------------------------------------------------

        tool_results = result.get(
            "tool_results",
            [],
        )

        tools_used = []

        for item in tool_results:

            tools_used.append(
                {
                    "tool": item.get("tool"),
                    "arguments": item.get(
                        "arguments",
                        {},
                    ),
                }
            )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return {
            "success": True,
            "data": {
                "resume_id": resume_id,
                "report": result.get(
                    "final_report",
                    "",
                ),
                "tools_used": tools_used,
                "research_rounds": result.get(
                    "research_rounds",
                    0,
                ),
            },
        }