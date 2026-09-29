import asyncio
import json
from typing import Any, TypedDict

from groq import AsyncGroq
from langgraph.graph import END, START, StateGraph

from backend.config.settings import settings
from backend.database.db import database
from backend.mcp.client import MCPClient


# ============================================================
# STATE
# ============================================================

class JobResearchState(TypedDict, total=False):
    user_id: str
    resume_id: str
    user_request: str

    messages: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]

    # Set when bounded research is sufficient. The final report
    # is generated separately, without tools, so the tool-calling
    # model cannot accidentally truncate the user-facing report.
    research_complete: bool
    final_report: str

    # Runtime-only object. It is never sent to Groq.
    _mcp_client: Any


# ============================================================
# SYSTEM PROMPT
# ============================================================

RESEARCH_SYSTEM_PROMPT = """
You are Placeko's Job Research Agent.

Your job is to gather evidence using MCP tools. Do NOT write the final
user-facing report yourself; a separate final-report step will do that.

RULES:
- Never invent candidate skills, projects, experience, or certifications.
- Use MCP tools instead of guessing.
- Resume evidence is the source of truth.
- "resume_gap" means the resume contains no evidence. It does NOT mean
  the candidate definitely lacks the skill.
- Use country="in" unless another country is explicitly requested.
- Do not repeat a tool call when the required information is already
  available.

BOUNDED RESEARCH WORKFLOW:

1. Call search_jobs once.
2. Inspect the returned jobs and identify important requirements.
3. Call search_resume_evidence using combined requirements.
   Maximum two evidence searches.
4. Readiness for fresh search results is handled by Placeko's application
   layer using analyze_fresh_job_readiness.
5. Do not call get_job_details during fresh job research.
6. Stop once enough evidence has been collected.

Do NOT search individual skills one by one. Prefer combined queries such
as: "Python FastAPI LLM RAG LangGraph backend".

Do not invent an overall fit score.
"""


# ============================================================
# FINAL REPORT PROMPT
# ============================================================

FINAL_REPORT_PROMPT = """
You are Placeko's final Job Research Report writer.

Create a concise, complete report from ONLY the supplied research data.
Do not invent information and do not claim that a candidate has a skill
unless the supplied resume evidence supports it.

Use this structure:

# Job Research Report

## 1. Relevant opportunities
For each of the top relevant jobs include:
- Job title — Company
- Location
- Why it is relevant, based on the actual job description and evidence

Use at most 5 jobs.

## 2. Candidate evidence
List concrete skills, projects, or experience supported by the resume.
Mention the project when useful.

## 3. Gaps / unverified requirements
Separate:
- requirements for which the resume contains no evidence
- requirements explicitly supported by the resume

Never convert a resume gap into a claim that the candidate lacks the skill.

## 4. Practical next steps
Give 3–5 concrete actions based only on the observed requirements and
resume gaps.

Important:
- Do not invent salary, experience requirements, dates, or technologies.
- Do not create a numerical fit score.
- Keep the report readable and complete.
- Prefer concise tables or bullets over long paragraphs.
"""


# ============================================================
# GROQ CLIENT
# ============================================================

groq_client = AsyncGroq(
    api_key=settings.GROQ_API_KEY
)


# ============================================================
# GROQ TOOL SCHEMAS
# ============================================================

# IDs are deliberately NOT model-controlled for tools that operate on
# user-specific stored data. The runtime injects the trusted values.
GROQ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_jobs",
            "description": "Search fresh job postings using Placeko's JSearch integration.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Concise job search query."},
                    "country": {"type": "string", "description": "Two-letter country code. Use 'in' for India.", "default": "in"},
                    "page": {"type": "integer", "description": "Search result page.", "default": 1},
                },
                "required": ["query"],
            },
        },
    },
]


# ============================================================
# MCP RESULT PARSER
# ============================================================

def _extract_mcp_result(result: Any) -> Any:
    if result is None:
        return None

    if getattr(result, "is_error", False):
        return {
            "error": True,
            "message": "MCP tool returned an error.",
        }

    content = getattr(result, "content", None)
    if not content:
        return None

    text_parts = []
    for item in content:
        if hasattr(item, "text"):
            text_parts.append(item.text)

    if not text_parts:
        return None

    combined = "\n".join(text_parts)

    try:
        return json.loads(combined)
    except json.JSONDecodeError:
        return combined


# ============================================================
# RESULT COMPACTION
# ============================================================

def compact_search_results(result: Any) -> Any:
    if not isinstance(result, list):
        return result

    jobs = []
    for job in result[:5]:
        if not isinstance(job, dict):
            continue

        skills = job.get("skills") or []
        if not isinstance(skills, list):
            skills = []

        jobs.append(
            {
                "job_id": job.get("job_id"),
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "employment_type": job.get("employment_type"),
                "experience": job.get("experience"),
                "salary": job.get("salary"),
                "skills": skills[:15],
                "description": (job.get("description") or "")[:700],
                "apply_url": job.get("apply_url"),
                "source": job.get("source"),
            }
        )

    return jobs


def compact_resume_evidence(result: Any) -> Any:
    if not isinstance(result, dict):
        return result

    output = dict(result)
    evidence = output.get("evidence")
    if isinstance(evidence, list):
        output["evidence"] = evidence[:10]

    return output


def compact_readiness(result: Any) -> Any:
    if not isinstance(result, dict):
        return result

    output = dict(result)
    readiness = output.get("readiness")

    if isinstance(readiness, dict):
        readiness_copy = dict(readiness)
        requirements = readiness_copy.get("requirements")

        if isinstance(requirements, list):
            readiness_copy["requirements"] = requirements[:10]

        output["readiness"] = readiness_copy

    return output


# ============================================================
# DETERMINISTIC RESEARCH HELPERS
# ============================================================

def _search_jobs_results(state: JobResearchState) -> list[dict[str, Any]]:
    for item in state.get("tool_results", []):
        if item.get("tool") == "search_jobs" and isinstance(item.get("result"), list):
            return item["result"]
    return []


def _build_evidence_query(jobs: list[dict[str, Any]]) -> str:
    """Build one grounded evidence query from actual returned jobs."""
    requirements: list[str] = []
    seen: set[str] = set()

    for job in jobs[:3]:
        for skill in job.get("skills", []) or []:
            if not isinstance(skill, str):
                continue
            value = skill.strip()
            key = value.lower()
            if value and key not in seen:
                seen.add(key)
                requirements.append(value)

    # Keep the query small enough for both MCP and the final context.
    preferred = [
        "Python", "FastAPI", "LLM", "RAG", "LangGraph", "LangChain",
        "PyTorch", "Machine Learning", "NLP", "Docker", "AWS",
    ]
    ordered = []
    for item in preferred + requirements:
        if item.lower() not in {x.lower() for x in ordered}:
            ordered.append(item)

    return " ".join(ordered[:10])


def _first_job(jobs: list[dict[str, Any]]) -> dict[str, Any] | None:
    for job in jobs:
        if isinstance(job, dict) and job.get("title"):
            return job
    return None


# ============================================================
# EXECUTE MCP TOOL
# ============================================================

async def execute_mcp_tool(
    client: MCPClient,
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:
    print(f"\n[AGENT] Calling MCP tool: {tool_name}")
    print(f"[AGENT] Arguments: {arguments}")

    result = await client.call_tool(tool_name, arguments)
    parsed = _extract_mcp_result(result)

    print(f"[AGENT] {tool_name} completed")
    return parsed


# ============================================================
# MODEL NODE — RESEARCH / TOOL SELECTION ONLY
# ============================================================

async def call_model(state: JobResearchState) -> dict[str, Any]:
    messages = list(state.get("messages", []))

    if not any(message.get("role") == "system" for message in messages):
        messages.insert(
            0,
            {
                "role": "system",
                "content": RESEARCH_SYSTEM_PROMPT,
            },
        )

    response = await groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        tools=GROQ_TOOLS,
        tool_choice="auto",
        max_tokens=500,
    )

    message = response.choices[0].message

    assistant_message: dict[str, Any] = {
        "role": "assistant",
        "content": message.content or "",
    }

    if message.tool_calls:
        assistant_message["tool_calls"] = []

        for tool_call in message.tool_calls:
            assistant_message["tool_calls"].append(
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
            )

    messages.append(assistant_message)

    return {
        "messages": messages,
    }


# ============================================================
# TOOL NODE
# ============================================================

async def execute_tools(state: JobResearchState) -> dict[str, Any]:
    """Execute the complete bounded research workflow deterministically."""
    messages = list(state.get("messages", []))
    tool_results = list(state.get("tool_results", []))

    # The CLI runner can inject a connected MCP client. The FastAPI
    # endpoint does not, so create a short-lived client for this run.
    client = state.get("_mcp_client")
    owns_client = False

    if client is None:
        client = MCPClient()
        await client.connect()
        owns_client = True
        print("\n[AGENT] MCP CLIENT CONNECTED (research node)")

    # Groq selects only the initial search query.
    last_message = messages[-1] if messages else {}
    tool_calls = last_message.get("tool_calls", [])
    search_call = next(
        (call for call in tool_calls if call["function"]["name"] == "search_jobs"),
        None,
    )

    if search_call is None:
        if owns_client:
            await client.close()
        return {"messages": messages, "tool_results": tool_results, "research_complete": True}

    try:
        arguments = json.loads(search_call["function"].get("arguments", "{}"))
    except json.JSONDecodeError:
        arguments = {}

    arguments.setdefault("country", "in")
    arguments.setdefault("page", 1)

    # 1. Fresh jobs
    search_result = await execute_mcp_tool(client, "search_jobs", arguments)
    search_result = compact_search_results(search_result)
    tool_results.append({"tool": "search_jobs", "arguments": arguments, "result": search_result})
    messages.append({
        "role": "tool",
        "tool_call_id": search_call["id"],
        "name": "search_jobs",
        "content": json.dumps(search_result, default=str),
    })

    jobs = search_result if isinstance(search_result, list) else []

    # 2. Grounded resume evidence
    evidence_query = _build_evidence_query(jobs)
    if evidence_query:
        evidence_arguments = {
            "user_id": state["user_id"],
            "resume_id": state["resume_id"],
            "query": evidence_query,
        }
        evidence_result = await execute_mcp_tool(
            client, "search_resume_evidence", evidence_arguments
        )
        tool_results.append({
            "tool": "search_resume_evidence",
            "arguments": evidence_arguments,
            "result": compact_resume_evidence(evidence_result),
        })

    # 3. Readiness against the exact fresh job returned above
    selected_job = _first_job(jobs)
    if selected_job is not None:
        readiness_arguments = {
            "user_id": state["user_id"],
            "resume_id": state["resume_id"],
            "job": selected_job,
        }
        readiness_result = await execute_mcp_tool(
            client, "analyze_fresh_job_readiness", readiness_arguments
        )
        tool_results.append({
            "tool": "analyze_fresh_job_readiness",
            "arguments": readiness_arguments,
            "result": compact_readiness(readiness_result),
        })

    # Never return to Groq after this point. That prevents repeated search calls.
    if owns_client:
        await client.close()
        print("[AGENT] MCP CLIENT DISCONNECTED (research node)")

    return {
        "messages": messages,
        "tool_results": tool_results,
        "research_complete": True,
    }


# ============================================================
# FINAL REPORT CONTEXT
# ============================================================

def build_final_context(state: JobResearchState) -> str:
    """Build a small, deterministic context for the final Groq call."""

    compact_results = []

    for item in state.get("tool_results", []):
        tool_name = item.get("tool")
        result = item.get("result")

        if tool_name == "search_jobs":
            result = compact_search_results(result)
        elif tool_name == "search_resume_evidence":
            result = compact_resume_evidence(result)
        elif tool_name in {"analyze_job_readiness", "analyze_fresh_job_readiness"}:
            result = compact_readiness(result)

        compact_results.append(
            {
                "tool": tool_name,
                "result": result,
            }
        )

    # Keep the final prompt safely below the large tool-conversation payload.
    serialized = json.dumps(
        compact_results,
        ensure_ascii=False,
        default=str,
    )

    return serialized[:12000]


# ============================================================
# FINAL REPORT NODE — NO TOOLS
# ============================================================

async def generate_final_report(
    state: JobResearchState,
) -> dict[str, Any]:
    context = build_final_context(state)

    final_messages = [
        {
            "role": "system",
            "content": FINAL_REPORT_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"User request:\n{state['user_request']}\n\n"
                "Research data from Placeko MCP tools:\n"
                f"{context}"
            ),
        },
    ]

    try:
        response = await groq_client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=final_messages,
            max_tokens=900,
            temperature=0.2,
        )

        report = (
            response.choices[0].message.content
            or "No final report generated."
        )

    except Exception as error:
        # A Groq quota/rate-limit failure must not turn a successful
        # MCP research run into an HTTP 500. Produce a deterministic
        # fallback from the actual collected data.
        if "429" not in str(error) and "rate limit" not in str(error).lower():
            raise

        jobs = []
        evidence = None
        readiness = None

        for item in state.get("tool_results", []):
            if item.get("tool") == "search_jobs":
                jobs = item.get("result") or []
            elif item.get("tool") == "search_resume_evidence":
                evidence = item.get("result")
            elif item.get("tool") == "analyze_fresh_job_readiness":
                readiness = item.get("result")

        lines = [
            "# Job Research Report",
            "",
            "## 1. Relevant opportunities",
        ]

        if jobs:
            for job in jobs[:5]:
                lines.append(
                    f"- {job.get('title', 'Unknown role')} — "
                    f"{job.get('company', 'Unknown company')} "
                    f"({job.get('location', 'Location not provided')})"
                )
        else:
            lines.append("- No job listings were returned.")

        lines.extend([
            "",
            "## 2. Candidate evidence",
        ])

        if isinstance(evidence, dict) and evidence.get("evidence"):
            for item in evidence["evidence"][:10]:
                lines.append(
                    f"- {item.get('source_type', 'evidence')}: "
                    f"{item.get('source', 'Unknown')} — "
                    f"{item.get('matched_text', '')}"
                )
        else:
            lines.append("- No matching grounded resume evidence was found.")

        lines.extend([
            "",
            "## 3. Gaps / unverified requirements",
        ])

        if isinstance(readiness, dict):
            readiness_data = readiness.get("readiness") or {}
            requirements = readiness_data.get("requirements") or []
            for req in requirements[:10]:
                lines.append(
                    f"- {req.get('requirement', 'Requirement')}: "
                    f"{req.get('status', 'unverified')} — "
                    f"{req.get('explanation', '')}"
                )
        else:
            lines.append("- Readiness analysis was not available.")

        lines.extend([
            "",
            "## 4. Practical next steps",
            "- Review the listed job requirements against the grounded resume evidence.",
            "- Address requirements marked as resume gaps or unverified.",
            "- Review the selected job's readiness evidence before applying.",
        ])

        report = "\n".join(lines)

    return {
        "final_report": report,
    }


# ============================================================
# ROUTER
# ============================================================

def route_after_model(state: JobResearchState) -> str:
    if state.get("research_complete"):
        return "final_report"

    messages = state.get("messages", [])

    if not messages:
        return "final_report"

    last_message = messages[-1]

    if last_message.get("tool_calls"):
        return "tools"

    # The research model has decided it has enough information.
    return "final_report"


# ============================================================
# GRAPH
# ============================================================

def build_research_graph():
    graph = StateGraph(JobResearchState)

    graph.add_node("model", call_model)
    graph.add_node("tools", execute_tools)
    graph.add_node("final_report", generate_final_report)

    graph.add_edge(START, "model")

    graph.add_conditional_edges(
        "model",
        route_after_model,
        {
            "tools": "tools",
            "final_report": "final_report",
        },
    )

    graph.add_conditional_edges(
        "tools",
        lambda state: (
            "final_report" if state.get("research_complete") else "model"
        ),
        {
            "model": "model",
            "final_report": "final_report",
        },
    )

    graph.add_edge("final_report", END)

    return graph.compile()


# ============================================================
# TEST RUNNER
# ============================================================

async def test_research_agent():
    if database.db is None:
        await database.connect_db()

    resume = await database.db["resumes"].find_one(
        {"is_active": True},
        sort=[("created_at", -1)],
    )

    if not resume:
        raise RuntimeError("No active resume found.")

    user_id = resume["user_id"]
    resume_id = str(resume["_id"])

    print("\nACTIVE RESUME")
    print(f"user_id: {user_id}")
    print(f"resume_id: {resume_id}")
    print(f"file_name: {resume.get('file_name')}")

    client = MCPClient()

    try:
        await client.connect()
        print("\nMCP CLIENT CONNECTED")

        graph = build_research_graph()

        user_request = (
            "Find relevant AI/ML and backend engineering jobs in India for my "
            "profile. Focus on Python, FastAPI, LLMs, RAG, LangGraph and "
            "backend development. Compare the jobs with evidence from my resume."
        )

        initial_state: JobResearchState = {
            "user_id": user_id,
            "resume_id": resume_id,
            "user_request": user_request,
            "messages": [
                {
                    "role": "user",
                    "content": user_request,
                }
            ],
            "tool_results": [],
            "research_complete": False,
            "_mcp_client": client,
        }

        result = await graph.ainvoke(
            initial_state,
            config={"recursion_limit": 12},
        )

        print("\n" + "=" * 70)
        print("FINAL JOB RESEARCH REPORT")
        print("=" * 70)
        print(result.get("final_report", "No final report generated."))

        print("\n" + "=" * 70)
        print("TOOLS USED")
        print("=" * 70)

        for item in result.get("tool_results", []):
            print(
                f"- {item['tool']} "
                f"{json.dumps(item['arguments'], default=str)}"
            )

    finally:
        await client.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(test_research_agent())
