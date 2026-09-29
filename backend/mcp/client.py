import asyncio
import os
from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self):
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        # MCP stdio subprocesses receive a restricted environment.
        # Explicitly pass the environment variables required by the
        # MCP server so it can connect to the same MongoDB instance
        # as the main FastAPI application.
        mcp_env = {}

        for key in (
            "MONGODB_URL",
            "DATABASE_NAME",
        ):
            value = os.getenv(key)
            if value is not None:
                mcp_env[key] = value

        server_params = StdioServerParameters(
            command="python",
            args=["-m", "backend.mcp.run_server"],
            env=mcp_env,
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

        return await self.session.call_tool(name, arguments)

    async def close(self):
        await self.exit_stack.aclose()