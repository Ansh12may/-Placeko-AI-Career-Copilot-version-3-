import asyncio

from bson import ObjectId

from backend.database.db import database


USER_ID = "6a74d7bdc079753af6122b5f"
RESUME_ID = "6a92a51780b4010468021d62"


async def main():
    await database.connect_db()

    resume = await database.db["resumes"].find_one(
        {
            "_id": ObjectId(RESUME_ID),
            "user_id": USER_ID,
        },
        {
            "_id": 1,
            "user_id": 1,
            "is_active": 1,
            "candidate_profile": 1,
        },
    )

    print("Resume found:", resume is not None)

    if resume:
        print("Resume ID:", resume.get("_id"))
        print("User ID:", resume.get("user_id"))
        print("Active:", resume.get("is_active"))
        print(
            "Has candidate_profile:",
            bool(resume.get("candidate_profile")),
        )

        profile = resume.get("candidate_profile") or {}

        print(
            "Profile keys:",
            list(profile.keys()),
        )

        print(
            "Skills:",
            profile.get("skills", [])[:10],
        )

    else:
        print(
            "No resume matched BOTH resume_id and user_id."
        )


if __name__ == "__main__":
    asyncio.run(main())