import asyncio

from backend.database.db import database


USER_ID = "6a74d7bdc079753af6122b5f"


async def main():
    await database.connect_db()

    resume = await database.db["resumes"].find_one(
        {
            "user_id": USER_ID,
        },
        {
            "_id": 1,
            "user_id": 1,
            "is_active": 1,
            "created_at": 1,
            "candidate_profile": 1,
        },
        sort=[("created_at", -1)],
    )

    if not resume:
        print("No resumes found for this user.")
        return

    print("Current resume:")
    print("resume_id:", str(resume["_id"]))
    print("user_id:", resume.get("user_id"))
    print("is_active:", resume.get("is_active"))
    print(
        "has_candidate_profile:",
        bool(resume.get("candidate_profile")),
    )

    profile = resume.get("candidate_profile") or {}

    print(
        "profile keys:",
        list(profile.keys()),
    )


if __name__ == "__main__":
    asyncio.run(main())