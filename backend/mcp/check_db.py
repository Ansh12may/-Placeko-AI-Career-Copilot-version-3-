import asyncio

from backend.database.db import database


USER_ID = "6a74d7bdc079753af6122b5f"
RESUME_ID = "6aa27615ff3ecf491cc05ca8"


async def main():
    await database.connect_db()

    document = await database.db["job_recommendations"].find_one(
        {
            "user_id": USER_ID,
            "resume_id": RESUME_ID,
        },
        {
            "user_id": 1,
            "resume_id": 1,
            "jobs.job_id": 1,
            "_id": 0,
        },
    )

    print("Recommendation document:")

    if document:
        print(document)
    else:
        print("No recommendation snapshot exists for the active resume.")

    # No close_db() here because your Database class
    # does not expose that method.


if __name__ == "__main__":
    asyncio.run(main())