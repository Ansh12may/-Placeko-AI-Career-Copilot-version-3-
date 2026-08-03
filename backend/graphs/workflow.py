from langgraph.graph import StateGraph, START, END
from backend.graphs.state import GraphState
from backend.agents.resume_agent import ResumeAgent
from backend.agents.job_search_agent import JobSearchAgent
builder = StateGraph(GraphState)
resume_agent = ResumeAgent()
job_search_agent = JobSearchAgent()
builder.add_node(
    "resume_agent",
    resume_agent.run,
)
builder.add_node(
    "job_search_agent",
    job_search_agent.run,
)
builder.add_edge(START, "resume_agent")
builder.add_edge("resume_agent","job_search_agent")
builder.add_edge("job_search_agent", END)
graph = builder.compile()