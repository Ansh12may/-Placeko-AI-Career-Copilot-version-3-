import asyncio
from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    Client for communicating with the Placeko MCP server.
    """

    def __init__(self):
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "backend.mcp.run_server"],
        )

        read_stream, write_stream = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await self.session.initialize()

    async def list_tools(self):
        if self.session is None:
            raise RuntimeError("MCP client is not connected.")

        result = await self.session.list_tools()

        return result.tools

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
    ):
        if self.session is None:
            raise RuntimeError("MCP client is not connected.")

        return await self.session.call_tool(
            name,
            arguments,
        )

    async def close(self):
        await self.exit_stack.aclose()