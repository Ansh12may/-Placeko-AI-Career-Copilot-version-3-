from langgraph.graph import StateGraph, START, END
from backend.graphs.state import GraphState
from backend.agents.resume_agent import ResumeAgent
builder = StateGraph(GraphState)
resume_agent = ResumeAgent()
builder.add_node(
    "resume_agent",
    resume_agent.run,
)
builder.add_edge(START, "resume_agent")
builder.add_edge("resume_agent", END)

graph = builder.compile()