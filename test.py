# from groq import Groq

# client = Groq()
# completion = client.chat.completions.create(
#     model="openai/gpt-oss-120b",
#     messages=[
#       {
#         "role": "user",
#         "content": ""
#       }
#     ],
#     temperature=1,
#     max_completion_tokens=2048,
#     top_p=1,
#     reasoning_effort="medium",
#     stream=True,
#     stop=None
# )

# for chunk in completion:
#     print(chunk.choices[0].delta.content or "", end="")

# from backend.tools.resume_parser import parse_resume

# text = parse_resume("/Users/ashutoshkushwaha/Desktop/Ashutosh_resume.pdf")
# print(text)
from backend.agents.job_search_agent import JobSearchAgent
from backend.schemas.candidate import CandidateProfile


def main():

    profile = CandidateProfile(
        name="Ashutosh",
        email="test@gmail.com",
        phone="+91xxxxxxxxxx",
        summary=None,
        skills=[
            "Python",
            "FastAPI",
            "LangGraph",
            "MongoDB"
        ],
        education=[],
        experience=[],
        projects=[],
        certifications=[],
    )

    state = {
        "messages": [],
        "resume_path": None,
        "resume_text": None,
        "candidate_profile": profile,
        "jobs": None,
        "ranked_jobs": None,
        "next_node": None,
        "error": None,
    }

    agent = JobSearchAgent()

    result = agent.run(state)

    jobs = result["jobs"]

    print("=" * 80)
    print(f"TOTAL JOBS FOUND : {len(jobs)}")
    print("=" * 80)

    for index, job in enumerate(jobs, start=1):

        print(f"\nJOB #{index}")
        print("-" * 80)

        print(f"Title       : {job.title}")
        print(f"Company     : {job.company}")
        print(f"Location    : {job.location}")
        print(f"Employment  : {job.employment_type}")
        print(f"Salary      : {job.salary}")
        print(f"Source      : {job.source}")
        print(f"Apply URL   : {job.apply_url}")


if __name__ == "__main__":
    main()