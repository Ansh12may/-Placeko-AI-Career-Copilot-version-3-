import asyncio

from backend.mcp.server import mcp
from backend.database.db import database


async def main():
    await database.connect_db()
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())