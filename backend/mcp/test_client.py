import asyncio

from backend.database.db import database
from backend.mcp.server import mcp


USER_ID = "6a74d7bdc079753af6122b5f"


async def main():
    await database.connect_db()

    # 1. Find the user's active resume
    resume = await database.db["resumes"].find_one(
        {
            "user_id": USER_ID,
            "is_active": True,
        }
    )

    if not resume:
        print("No active resume found.")
        return

    resume_id = str(resume["_id"])

    print("Active resume:", resume_id)

    # 2. Find recommendations generated for this resume
    recommendations = await database.db["job_recommendations"].find_one(
        {
            "user_id": USER_ID,
            "resume_id": resume_id,
        }
    )

    if not recommendations:
        print("No recommendation snapshot found.")
        return

    jobs = [
        job
        for job in recommendations.get("jobs", [])
        if job.get("job_id")
    ]

    if not jobs:
        print("No valid jobs with job_id found.")
        return

    job_id = jobs[0]["job_id"]

    print("Testing job:", job_id)

    # 3. Get the registered MCP tools
    tools = {
        tool.name: tool
        for tool in mcp._tool_manager.list_tools()
    }

    print("\nRegistered tools:")
    for name in tools:
        print("-", name)

    # 4. Test get_job_details
    print("\n--- get_job_details ---")

    result = await tools["get_job_details"].fn(
        user_id=USER_ID,
        resume_id=resume_id,
        job_id=job_id,
    )

    print(result)

    # 5. Test resume evidence
    print("\n--- search_resume_evidence ---")

    result = await tools["search_resume_evidence"].fn(
        user_id=USER_ID,
        resume_id=resume_id,
        query="Python",
    )

    print(result)

    # 6. Test readiness analysis
    print("\n--- analyze_job_readiness ---")

    result = await tools["analyze_job_readiness"].fn(
        user_id=USER_ID,
        resume_id=resume_id,
        job_id=job_id,
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
