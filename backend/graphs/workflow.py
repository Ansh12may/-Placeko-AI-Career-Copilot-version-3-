from langgraph.graph import StateGraph, START, END

from backend.graphs.state import GraphState
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

recommendation_agent = RecommendationAgent()


# =========================================================
# Register Nodes
# =========================================================

builder.add_node(
    "recommendation_agent",
    recommendation_agent.run,
)


# =========================================================
# Define Workflow
# =========================================================

builder.add_edge(
    START,
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