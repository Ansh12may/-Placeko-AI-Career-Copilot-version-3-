import sys
from motor.motor_asyncio import AsyncIOMotorClient
from backend.config.settings import settings


class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient | None = None
        self.db = None

    async def connect_db(self):
        self.client = AsyncIOMotorClient(
            settings.MONGODB_URL
        )

        await self.client.admin.command("ping")

        self.db = self.client[
            settings.DATABASE_NAME
        ]

        print(
            "MongoDB Connected",
            file=sys.stderr,
        )

    async def disconnect_db(self):
        if self.client:
            self.client.close()

            print(
                "MongoDB Disconnected",
                file=sys.stderr,
            )


database = Database()
