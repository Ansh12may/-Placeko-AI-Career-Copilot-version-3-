import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "backend.mcp.run_server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            print("\nMCP SERVER CONNECTED")

            result = await session.call_tool(
                "search_jobs",
                {
                    "query": "AI Engineer Python FastAPI",
                    "country": "in",
                    "page": 1,
                },
            )

            print("\nSEARCH JOBS RESULT:")

            for content in result.content:
                if hasattr(content, "text"):
                    print(content.text)


if __name__ == "__main__":
    asyncio.run(main())