from langgraph.graph import StateGraph, START, END

from backend.graphs.state import GraphState

from backend.Jobs.agents.job_search_agent import (
    JobSearchAgent,
)

from backend.Jobs.agents.recommendation_agent import (
    RecommendationAgent,
)


# =========================================================
# Create Graph
# =========================================================

builder = StateGraph(GraphState)


# =========================================================
# Initialize Agents
# =========================================================

job_search_agent = JobSearchAgent()

recommendation_agent = RecommendationAgent()


# =========================================================
# Register Nodes
# =========================================================

builder.add_node(
    "job_search_agent",
    job_search_agent.run,
)

builder.add_node(
    "recommendation_agent",
    recommendation_agent.run,
)


# =========================================================
# Define Workflow
# =========================================================

builder.add_edge(
    START,
    "job_search_agent",
)

builder.add_edge(
    "job_search_agent",
    "recommendation_agent",
)

builder.add_edge(
    "recommendation_agent",
    END,
)


# =========================================================
# Compile Graph
# =========================================================

graph = builder.compile()