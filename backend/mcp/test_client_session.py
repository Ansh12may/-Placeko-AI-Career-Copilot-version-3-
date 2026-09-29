import asyncio

from backend.mcp.client import MCPClient


async def main():
    client = MCPClient()

    try:
        await client.connect()

        print("\nMCP CLIENT CONNECTED")

        tools = await client.list_tools()

        print("\nAVAILABLE TOOLS:")
        for tool in tools:
            print(f"- {tool.name}")

        result = await client.call_tool(
            "search_jobs",
            {
                "query": "AI Engineer Python FastAPI",
                "country": "in",
                "page": 1,
            },
        )

        print("\nSEARCH RESULT:")

        for content in result.content:
            if hasattr(content, "text"):
                print(content.text)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())