import asyncio

from backend.database.db import database
from backend.Resume.repositories.resume_repository import ResumeRepository


async def main():
    user_id = "6a7714f33cb53bf1ddf7e253"
    resume_id = "6a776b91bcd34917c9e1f1ec"

    try:
        # Connect directly because the FastAPI application is not running.
        await database.connect_db()

        repository = ResumeRepository()

        resume = await repository.get_resume_by_id(
            resume_id=resume_id,
            user_id=user_id,
        )

        if not resume:
            print("\nRESUME NOT FOUND")
            return

        print("\n" + "=" * 70)
        print("STORED RESUME KEYS")
        print("=" * 70)

        print(list(resume.keys()))

        print("\n" + "=" * 70)
        print("CANDIDATE PROFILE")
        print("=" * 70)

        profile = resume.get("candidate_profile")

        if profile is None:
            print("candidate_profile = None")
        else:
            print(profile)

        print("\n" + "=" * 70)
        print("TECHNOLOGY CHECK")
        print("=" * 70)

        profile_text = str(profile).lower()

        technologies = [
            "python",
            "fastapi",
            "langchain",
            "langgraph",
            "rag",
            "llm",
            "pinecone",
            "react",
            "mongodb",
            "pytorch",
            "scikit-learn",
        ]

        for technology in technologies:
            status = "FOUND" if technology in profile_text else "MISSING"
            print(f"{technology:15} -> {status}")

        print("\n" + "=" * 70)

    finally:
        await database.disconnect_db()


if __name__ == "__main__":
    asyncio.run(main())