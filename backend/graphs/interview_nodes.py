"""
Interview Graph Adapter Nodes

AnswerEvaluationAgent and InterviewReportAgent operate on an
InterviewSession object directly rather than on GraphState,
because they were originally built to be called straight from
InterviewService instead of through the shared LangGraph workflow.

These adapter nodes bridge that gap so both agents can participate
as ordinary graph nodes without changing their own code:

- read InterviewSession out of GraphState["interview_session"]
- run the underlying agent
- write the updated InterviewSession back into GraphState

AnswerEvaluationAgent / InterviewReportAgent stay untouched and
remain independently reusable/testable outside the graph.
"""

from backend.graphs.state import GraphState

from backend.Interview.agents.answer_evaluation_agent import (
    AnswerEvaluationAgent,
)

from backend.Interview.agents.interview_report_agent import (
    InterviewReportAgent,
)


answer_evaluation_agent = AnswerEvaluationAgent()
interview_report_agent = InterviewReportAgent()


def evaluate_answer_node(state: GraphState) -> GraphState:
    """
    Evaluate the candidate's most recent answer.

    Expects state["interview_session"] to be an InterviewSession
    whose current QuestionAnswerPair already has `answer` set
    (InterviewService sets this before invoking the graph).
    """

    session = state.get("interview_session")

    if session is None:
        raise ValueError(
            "interview_session missing from GraphState."
        )

    session = answer_evaluation_agent.run(session)

    state["interview_session"] = session

    return state


def generate_report_node(state: GraphState) -> GraphState:
    """
    Generate the final interview report for a completed session.
    """

    session = state.get("interview_session")

    if session is None:
        raise ValueError(
            "interview_session missing from GraphState."
        )

    session = interview_report_agent.run(session)

    state["interview_session"] = session

    return state
