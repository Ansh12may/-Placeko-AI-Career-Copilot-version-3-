from mcp.server import MCPServer

from backend.database.db import database

mcp = MCPServer("Placeko Job Intelligence")

from backend.mcp.tools import job_tools


async def initialize_database():
    if database.db is None:
        await database.connect_db()