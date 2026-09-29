from langchain_core.tools import tool

from backend.config.settings import settings


@tool
def test_search(query: str) -> str:
    """Search for jobs matching a query."""
    return query


llm = settings.llm.bind_tools([test_search])

response = llm.invoke(
    "Find AI backend jobs using Python."
)

print(response)
print(response.tool_calls)