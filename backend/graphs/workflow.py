from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.memory import (
    InMemorySaver,
)

from backend.graphs.state import GraphState

from backend.Jobs.agents.job_search_agent import (
    JobSearchAgent,
)

from backend.Jobs.agents.recommendation_agent import (
    RecommendationAgent,
)

from backend.Applications.agents.application_agent import (
    ApplicationAgent,
)

from backend.Applications.agents.application_approval_agent import (
    ApplicationApprovalAgent,
)

from backend.Applications.agents.application_executor_agent import (
    ApplicationExecutorAgent,
)
from backend.Jobs.agents.job_reranking_agent import (
    JobRerankingAgent,
)

from backend.Resume.agents.resume_agent import (
    ResumeAgent,
)

from backend.ATS.agents.resume_analysis_agent import (
    ResumeAnalysisAgent,
)

from backend.Interview.agents.interview_planner_agent import (
    InterviewPlannerAgent,
)

from backend.Interview.agents.question_generator_agent import (
    QuestionGeneratorAgent,
)

from backend.graphs.interview_nodes import (
    evaluate_answer_node,
    generate_report_node,
)

# Initialize Agents

job_search_agent = JobSearchAgent()
recommendation_agent = RecommendationAgent()
job_reranking_agent = JobRerankingAgent()
application_agent = ApplicationAgent()
application_approval_agent = (
    ApplicationApprovalAgent()
)

application_executor_agent = (
    ApplicationExecutorAgent()
)

resume_agent = ResumeAgent()
resume_analysis_agent = ResumeAnalysisAgent()

interview_planner_agent = InterviewPlannerAgent()
question_generator_agent = QuestionGeneratorAgent()



# Workflow Router


def workflow_router(
    state: GraphState,
) -> str:

    workflow_type = state.get(
        "workflow_type"
    )

    if workflow_type == "application":
        return "application_agent"

    if workflow_type == "recommendation":
        return "job_search_agent"

    if workflow_type == "resume_analysis":
        return "resume_agent"

    if workflow_type == "interview_plan":
        return "interview_planner_agent"

    if workflow_type == "interview_next_question":
        return "question_generator_agent"

    if workflow_type == "interview_evaluate_answer":
        return "evaluate_answer_node"

    if workflow_type == "interview_report":
        return "generate_report_node"

    raise ValueError(
        f"Unsupported workflow type: {workflow_type}"
    )



# Application Approval Router


def application_approval_router(
    state: GraphState,
) -> str:

    human_approval = state.get(
        "human_approval"
    )

    if human_approval is True:
        return "application_executor_agent"

    if human_approval is False:
        return END

    raise ValueError(
        "Human approval decision is missing."
    )



# Create Graph

builder = StateGraph(
    GraphState
)



# Register Nodes


builder.add_node(
    "job_search_agent",
    job_search_agent.run,
)

builder.add_node(
    "recommendation_agent",
    recommendation_agent.run,
)

builder.add_node(
    "job_reranking_agent",
    job_reranking_agent.run,
)

builder.add_node(
    "application_agent",
    application_agent.run,
)

builder.add_node(
    "application_approval_agent",
    application_approval_agent.run,
)

builder.add_node(
    "application_executor_agent",
    application_executor_agent.run,
)

builder.add_node(
    "resume_agent",
    resume_agent.run,
)

builder.add_node(
    "resume_analysis_agent",
    resume_analysis_agent.run,
)

builder.add_node(
    "interview_planner_agent",
    interview_planner_agent.run,
)

builder.add_node(
    "question_generator_agent",
    question_generator_agent.run,
)

builder.add_node(
    "evaluate_answer_node",
    evaluate_answer_node,
)

builder.add_node(
    "generate_report_node",
    generate_report_node,
)



# START → Workflow Router


builder.add_conditional_edges(
    START,
    workflow_router,
    {
        "job_search_agent":
            "job_search_agent",

        "application_agent":
            "application_agent",

        "resume_agent":
            "resume_agent",

        "interview_planner_agent":
            "interview_planner_agent",

        "question_generator_agent":
            "question_generator_agent",

        "evaluate_answer_node":
            "evaluate_answer_node",

        "generate_report_node":
            "generate_report_node",
    },
)



# Recommendation Workflow


builder.add_edge(
    "job_search_agent",
    "recommendation_agent",
)

builder.add_edge(
    "recommendation_agent",
    "job_reranking_agent",
)

builder.add_edge(
    "job_reranking_agent",
    END,
)



# Application Workflow


builder.add_edge(
    "application_agent",
    "application_approval_agent",
)


builder.add_conditional_edges(
    "application_approval_agent",
    application_approval_router,
    {
        "application_executor_agent":
            "application_executor_agent",

        END:
            END,
    },
)


builder.add_edge(
    "application_executor_agent",
    END,
)



# Resume Analysis Workflow


builder.add_edge(
    "resume_agent",
    "resume_analysis_agent",
)

builder.add_edge(
    "resume_analysis_agent",
    END,
)


# =========================================================
# Interview Workflow
#
# Each of these is a single-node workflow rather than a chain:
# InterviewService runs its own business logic (question-count
# normalization, completion checks, category selection) between
# planning, question generation, evaluation, and reporting, so
# those steps can't be fused into one graph traversal without
# duplicating that logic inside the graph. "interview_plan" runs
# once at interview start; "interview_next_question" is reused
# both for the first question and every question after an answer.
# =========================================================

builder.add_edge(
    "interview_planner_agent",
    END,
)

builder.add_edge(
    "question_generator_agent",
    END,
)

builder.add_edge(
    "evaluate_answer_node",
    END,
)

builder.add_edge(
    "generate_report_node",
    END,
)



# Checkpointer


checkpointer = InMemorySaver()



# Compile Graph


graph = builder.compile(
    checkpointer=checkpointer
)