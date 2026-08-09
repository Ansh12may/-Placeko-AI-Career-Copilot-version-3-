
# from backend.Resume.tools.resume_parser import parse_resume
# from backend.Resume.agents.resume_agent import ResumeAgent
# text = parse_resume("/Users/ashutoshkushwaha/Desktop/Ashutosh_resume.pdf")

# from backend.Jobs.agents.job_search_agent import JobSearchAgent
# from backend.Resume.schemas.candidate import CandidateProfile


# def main():

#     profile = CandidateProfile(
#         name="Ashutosh",
#         email="test@gmail.com",
#         phone="+91xxxxxxxxxx",
#         summary=None,
#         skills=[
#             "Python",
#             "FastAPI",
#             "LangGraph",
#             "MongoDB"
#         ],
#         education=[],
#         experience=[],
#         projects=[],
#         certifications=[],
#     )

#     state = {
#         "messages": [],
#         "resume_path": None,
#         "resume_text": None,
#         "candidate_profile": profile,
#         "jobs": None,
#         "ranked_jobs": None,
#         "next_node": None,
#         "error": None,
#     }

#     agent = JobSearchAgent()

#     result = agent.run(state)

#     jobs = result["jobs"]

#     print("=" * 80)
#     print(f"TOTAL JOBS FOUND : {len(jobs)}")
#     print("=" * 80)

#     for index, job in enumerate(jobs, start=1):

#         print(f"\nJOB #{index}")
#         print("-" * 80)

#         print(f"Title       : {job.title}")
#         print(f"Company     : {job.company}")
#         print(f"Location    : {job.location}")
#         print(f"Employment  : {job.employment_type}")
#         print(f"Salary      : {job.salary}")
#         print(f"Source      : {job.source}")
#         print(f"Apply URL   : {job.apply_url}")


# if __name__ == "__main__":
#     main()


# from backend.Jobs.tools.embedding_tool import EmbeddingTool
# tool = EmbeddingTool()
# embedding = tool.get_embedding(
#     "Python FastAPI MongoDB LangGraph"

# )
# print(type(embedding))
# print(len(embedding))
# print(embedding[:10])


# # from backend.services.similarity_service import SimilarityService

# # service = SimilarityService()

# # v1 = [1, 2, 3]

# # v2 = [1, 2, 3]

# # v3 = [3, 1, 0]

# # print(service.cosine_similarity(v1, v2))

# # print(service.cosine_similarity(v1, v3))


# from backend.Jobs.agents.job_ranking_agent import JobRankingAgent
# from backend.graphs.state import GraphState
# from backend.Resume.schemas.candidate import CandidateProfile
# from backend.Jobs.schemas.job import Job

# profile = CandidateProfile(
#     name="Ashutosh",
#     email="test@gmail.com",
#     phone="+91xxxxxxxxxx",
#     skills=[
#         "Python",
#         "FastAPI",
#         "MongoDB",
#         "LangGraph"
#     ],
#     education=[],
#     experience=[],
#     projects=[],
#     certifications=[]
# )

# jobs = [
#     Job(
#         title="Python Backend Developer",
#         company="ABC",
#         location="Bangalore",
#         employment_type="Full-time",
#         experience=None,
#         salary="10 LPA",
#         skills=[],
#         description="Python FastAPI MongoDB Docker REST API",
#         apply_url="https://example.com",
#         source="LinkedIn",
#     ),
#     Job(
#         title="Frontend React Developer",
#         company="XYZ",
#         location="Delhi",
#         employment_type="Full-time",
#         experience=None,
#         salary="8 LPA",
#         skills=[],
#         description="React Next.js TypeScript Tailwind CSS",
#         apply_url="https://example.com",
#         source="LinkedIn",
#     ),
# ]

# state = GraphState(
#     candidate_profile=profile,
#     jobs=jobs,
# )

# agent = JobRankingAgent()

# result = agent.run(state)

# for job in result["jobs"]:
#     print(job.title,job.match_score)


# from backend.Jobs.tools.reranker_tool import RerankerTool
# reranker = RerankerTool()
# resume = """
# Python FastAPI MongoDB LangGraph REST APIs
# """
# job = """
# We are looking for a Backend Developer with
# Python, FastAPI, PostgreSQL and Docker.
# """
# score = reranker.score(resume, job)
# print(score)






# """
# Test Resume Analysis Pipeline
# """

# from backend.graphs.state import GraphState
# from backend.agents.resume_analysis_agent import ResumeAnalysisAgent
# from backend.schemas.candidate import (
#     CandidateProfile,
#     Education,
#     Experience,
#     Project,
# )

# # ----------------------------------------------------
# # Create Dummy Candidate
# # ----------------------------------------------------

# candidate = CandidateProfile(
#     name="Ashutosh Kushwaha",

#     email="ashutosh@gmail.com",

#     phone="9876543210",

#     linkedin="https://linkedin.com/in/ashutosh",

#     github="https://github.com/ashutosh",

#     summary=(
#         "Final-year AI/ML student interested in Backend "
#         "Development, LLMs, FastAPI and Agentic AI."
#     ),

#     skills=[
#         "Python",
#         "FastAPI",
#         "MongoDB",
#         "Docker",
#         "LangGraph",
#         "Machine Learning",
#         "Deep Learning",
#         "Git",
#         "REST API",
#         "SQL",
#     ],

#     education=[
#         Education(
#             degree="B.Tech CSE (AI & ML)",
#             institution="Bennett University",
#             year="2027",
#         )
#     ],

#     experience=[
#         Experience(
#             role="AI Intern",
#             company="ABC Technologies",
#             description=(
#                 "Built AI backend services using FastAPI "
#                 "and LangGraph."
#             ),
#         )
#     ],

#     projects=[
#         Project(
#             title="CareerCopilot",

#             description=(
#                 "AI-powered career assistant with resume "
#                 "analysis and intelligent job recommendations."
#             ),

#             technologies=[
#                 "Python",
#                 "FastAPI",
#                 "LangGraph",
#                 "Pinecone",
#             ],
#         ),

#         Project(
#             title="Medical Chatbot",

#             description=(
#                 "LLM-powered chatbot using RAG architecture."
#             ),

#             technologies=[
#                 "Python",
#                 "LangChain",
#                 "FAISS",
#             ],
#         ),
#     ],

#     certifications=[
#         "AWS Cloud Practitioner",
#         "Google AI Essentials",
#     ],
# )

# # ----------------------------------------------------
# # Build GraphState
# # ----------------------------------------------------

# state = GraphState(
#     candidate_profile=candidate,
# )

# # ----------------------------------------------------
# # Run Agent
# # ----------------------------------------------------

# agent = ResumeAnalysisAgent()

# state = agent.run(state)

# report = state["ats_report"]

# # ----------------------------------------------------
# # Print Report
# # ----------------------------------------------------

# print("=" * 70)
# print("ATS REPORT")
# print("=" * 70)

# print(f"\nOverall Score : {report.overall_score}/100")

# print("\nSection Scores")
# print("-" * 70)

# print(
#     f"Contact Information : "
#     f"{report.contact_information.score}/"
#     f"{report.contact_information.max_score}"
# )

# print(
#     f"Education          : "
#     f"{report.education.score}/"
#     f"{report.education.max_score}"
# )

# print(
#     f"Experience         : "
#     f"{report.experience.score}/"
#     f"{report.experience.max_score}"
# )

# print(
#     f"Projects           : "
#     f"{report.projects.score}/"
#     f"{report.projects.max_score}"
# )

# print(
#     f"Skills             : "
#     f"{report.skills.score}/"
#     f"{report.skills.max_score}"
# )

# print(
#     f"Summary            : "
#     f"{report.summary.score}/"
#     f"{report.summary.max_score}"
# )

# print(
#     f"Formatting         : "
#     f"{report.formatting.score}/"
#     f"{report.formatting.max_score}"
# )

# print("\n" + "=" * 70)

# print("\nStrengths")
# for item in report.strengths:
#     print(f"✓ {item}")

# print("\nWeaknesses")
# for item in report.weaknesses:
#     print(f"✗ {item}")

# print("\nMissing Keywords")
# for item in report.missing_keywords:
#     print(f"• {item}")

# print("\nFormatting Feedback")
# for item in report.formatting_feedback:
#     print(f"• {item}")

# print("\nEducation Feedback")
# for item in report.education_feedback:
#     print(f"• {item}")

# print("\nExperience Feedback")
# for item in report.experience_feedback:
#     print(f"• {item}")

# print("\nProject Feedback")
# for item in report.project_feedback:
#     print(f"• {item}")

# print("\nSkills Feedback")
# for item in report.skills_feedback:
#     print(f"• {item}")

# print("\nRecommendations")
# for i, item in enumerate(report.recommendations, start=1):
#     print(f"{i}. {item}")

# print("\n" + "=" * 70)
# print("PIPELINE COMPLETED SUCCESSFULLY")
# print("=" * 70)


"""
Test Interview Planner Agent
"""

# from backend.agents.interview_planner_agent import InterviewPlannerAgent

# from backend.schemas.candidate import (
#     CandidateProfile,
#     Education,
#     Experience,
#     Project,
# )

# from backend.schemas.job import Job

# from backend.schemas.interview_plan import (
#     InterviewMode,
#     DifficultyLevel,
# )


# # ==========================================================
# # Candidate
# # ==========================================================

# candidate = CandidateProfile(

#     name="Ashutosh Kushwaha",

#     email="ashutosh@gmail.com",

#     phone="9876543210",

#     summary=(
#         "Final-year AI/ML student passionate about "
#         "Backend Development, FastAPI, LLMs and Agentic AI."
#     ),

#     skills=[
#         "Python",
#         "FastAPI",
#         "LangGraph",
#         "LangChain",
#         "MongoDB",
#         "Docker",
#         "REST API",
#         "Machine Learning",
#         "Deep Learning",
#     ],

#     education=[
#         Education(
#             institution="Bennett University",
#             degree="B.Tech CSE (AI/ML)",
#             year="2027",
#         )
#     ],

#     experience=[
#         Experience(
#             company="ABC Technologies",
#             role="AI Intern",
#             duration="3 Months",
#             description=(
#                 "Built backend AI services using "
#                 "FastAPI, LangGraph and MongoDB."
#             ),
#         )
#     ],

#     projects=[
#         Project(
#             title="CareerCopilot",

#             technologies=[
#                 "Python",
#                 "FastAPI",
#                 "LangGraph",
#                 "Pinecone",
#                 "MongoDB",
#             ],

#             description=(
#                 "AI-powered career assistant with "
#                 "resume analysis, ATS scoring and "
#                 "semantic job recommendation."
#             ),
#         ),

#         Project(
#             title="Medical Chatbot",

#             technologies=[
#                 "RAG",
#                 "LangChain",
#                 "FAISS",
#             ],

#             description=(
#                 "Medical chatbot using Retrieval "
#                 "Augmented Generation."
#             ),
#         ),
#     ],

#     certifications=[
#         "AWS Cloud Practitioner",
#         "Google AI Essentials",
#     ],
# )

# # ==========================================================
# # Target Job
# # ==========================================================

# job = Job(

#     title="Backend AI Engineer",

#     company="OpenAI",

#     location="Remote",

#     employment_type="Internship",

#     skills=[
#         "Python",
#         "FastAPI",
#         "Docker",
#         "REST API",
#         "LangGraph",
#         "MongoDB",
#         "AWS",
#     ],

#     description="""
# Looking for an AI Backend Engineer with strong Python,
# FastAPI, REST APIs, Docker and LLM experience.
# Knowledge of LangGraph, Vector Databases,
# and scalable backend systems is preferred.
# """,

#     salary=None,

#     apply_url="https://example.com",
#     source="LinkedIn",

# )

# # ==========================================================
# # GraphState
# # ==========================================================

# state = {

#     "candidate_profile": candidate,

#     "selected_job": job,

#     "interview_mode": InterviewMode.MIXED,

#     "difficulty": DifficultyLevel.MEDIUM,

# }

# # ==========================================================
# # Run Agent
# # ==========================================================

# agent = InterviewPlannerAgent()

# state = agent.run(state)

# plan = state["interview_plan"]

# # ==========================================================
# # Print Result
# # ==========================================================

# print("=" * 70)
# print("INTERVIEW PLAN")
# print("=" * 70)

# print()

# print("Interview Mode :", plan.interview_mode.value)
# print("Difficulty     :", plan.difficulty.value)
# print("Duration       :", plan.duration_minutes, "minutes")

# print()

# print("Technical Questions :", plan.technical_questions)
# print("Behavioral Questions:", plan.behavioral_questions)
# print("Project Questions   :", plan.project_questions)
# print("Follow-up Questions :", plan.followup_questions)

# print()

# print("Focus Topics")

# for topic in plan.focus_topics:
#     print("-", topic)

# print()

# print("Evaluation Criteria")

# for criterion in plan.evaluation_criteria:
#     print("-", criterion)

# print()

# print("Interviewer Notes")
# print("-" * 70)
# print(plan.interviewer_notes)

# print()
# print("=" * 70)
# print("PIPELINE COMPLETED SUCCESSFULLY")
# print("=" * 70)


# """
# Test Phase 5.2
# Question Generator
# """

# from backend.Interview.agents.question_generator_agent import QuestionGeneratorAgent
# from backend.Interview.schemas.interview_plan import (
#     InterviewPlan,
#     InterviewMode,
#     DifficultyLevel,
# )
# from backend.Interview.schemas.interview_question import QuestionCategory

# from backend.Resume.schemas.candidate import (
#     CandidateProfile,
#     Education,
#     Experience,
#     Project,
# )

# from backend.Jobs.schemas.job import Job


# # ==========================================================
# # Candidate
# # ==========================================================

# candidate = CandidateProfile(

#     name="Ashutosh Kushwaha",

#     email="ashutosh@gmail.com",

#     phone="9876543210",

#     summary="Final-year AI/ML student passionate about Backend AI.",

#     skills=[
#         "Python",
#         "FastAPI",
#         "LangGraph",
#         "MongoDB",
#         "Docker",
#         "REST API",
#         "Pinecone",
#         "Machine Learning",
#     ],

#     education=[
#         Education(
#             institution="Bennett University",
#             degree="B.Tech CSE AI/ML",
#             year="2027",
#         )
#     ],

#     experience=[
#         Experience(
#             company="ABC Technologies",
#             role="AI Intern",
#             duration="3 Months",
#             description="Built AI backend services using FastAPI and LangGraph.",
#         )
#     ],

#     projects=[
#         Project(
#             title="CareerCopilot",

#             technologies=[
#                 "Python",
#                 "FastAPI",
#                 "LangGraph",
#                 "MongoDB",
#                 "Pinecone",
#             ],

#             description=(
#                 "AI-powered career assistant "
#                 "for ATS analysis and job recommendations."
#             ),
#         ),

#         Project(
#             title="Medical Chatbot",

#             technologies=[
#                 "LangChain",
#                 "RAG",
#                 "FAISS",
#             ],

#             description="Medical chatbot using Retrieval Augmented Generation.",
#         ),
#     ],

#     certifications=[
#         "AWS Cloud Practitioner",
#         "Google AI Essentials",
#     ],
# )

# # ==========================================================
# # Job
# # ==========================================================

# job = Job(

#     title="Backend AI Engineer",

#     company="OpenAI",

#     location="Remote",

#     employment_type="Internship",

#     skills=[
#         "Python",
#         "FastAPI",
#         "Docker",
#         "MongoDB",
#         "REST API",
#         "LangGraph",
#     ],

#     description="""
# Looking for a Backend AI Engineer with strong
# FastAPI, Docker, MongoDB, REST APIs,
# LangGraph and scalable backend development experience.
# """,

#     salary=None,

#     apply_url="https://example.com",

#     source="LinkedIn",
# )

# # ==========================================================
# # Interview Plan
# # ==========================================================

# plan = InterviewPlan(

#     interview_mode=InterviewMode.MIXED,

#     difficulty=DifficultyLevel.MEDIUM,

#     duration_minutes=45,

#     technical_questions=4,

#     behavioral_questions=2,

#     project_questions=2,

#     followup_questions=5,

#     focus_topics=[
#         "Python",
#         "FastAPI",
#         "LangGraph",
#         "MongoDB",
#         "Docker",
#     ],

#     evaluation_criteria=[
#         "Problem Solving",
#         "Communication",
#         "Technical Accuracy",
#         "System Design",
#     ],

#     interviewer_notes=(
#         "Focus on backend architecture and project discussions."
#     ),
# )

# # ==========================================================
# # Graph State
# # ==========================================================

# state = {

#     "candidate_profile": candidate,

#     "selected_job": job,

#     "interview_plan": plan,

#     "question_number": 1,

#     "current_category": QuestionCategory.TECHNICAL,

#     "previous_questions": [],
# }

# # ==========================================================
# # Run Agent
# # ==========================================================

# agent = QuestionGeneratorAgent()

# state = agent.run(state)

# question = state["current_question"]

# # ==========================================================
# # Print
# # ==========================================================

# print("=" * 70)
# print("INTERVIEW QUESTION")
# print("=" * 70)

# print()

# print("Question ID :", question.question_id)
# print("Category    :", question.category.value)
# print("Difficulty  :", question.difficulty.value)

# print()

# print("Question")
# print("-" * 70)
# print(question.question)

# print()

# print("Focus Topic")
# print("-" * 70)
# print(question.focus_topic)

# print()

# print("Expected Topics")
# print("-" * 70)

# for topic in question.expected_topics:
#     print("•", topic)

# print()

# print("Follow-up Allowed")
# print("-" * 70)
# print(question.followup_allowed)

# print()

# print("Estimated Time")
# print("-" * 70)
# print(question.estimated_time_seconds, "seconds")

# print()

# print("Interviewer Notes")
# print("-" * 70)
# print(question.interviewer_notes)

# print()

# print("=" * 70)
# print("PIPELINE COMPLETED SUCCESSFULLY")
# print("=" * 70)



"""
Integration Test
Job Recommendation Pipeline
"""

"""
Test Interview Planner Service

Flow

Resume -> CandidateProfile
            ↓
Job Search -> Job
            ↓
Interview Planner
            ↓
InterviewPlan
"""

# from pprint import pprint
# from backend.graphs.workflow import graph
# from backend.Interview.services.interview_planner_service import (
#     InterviewPlannerService,
# )
# import pathlib

# from backend.Interview.schemas.interview_plan import (
#     InterviewMode,
#     DifficultyLevel,
# )


# RESUME_PATH = "/Users/ashutoshkushwaha/Desktop/Ashutosh_resume.pdf"    # <-- change to your resume path


# def main():

#     state = {
#         "messages": [],
#         "resume_path": RESUME_PATH,
#     }

#     print("=" * 80)
#     print("Running Resume + Job Graph...")
#     print("=" * 80)

#     state = graph.invoke(state)

#     profile = state["candidate_profile"]

#     ranked_jobs = state["ranked_jobs"]

#     if not ranked_jobs:
#         raise ValueError(
#             "No jobs were returned by JobSearchAgent."
#         )

#     selected_job = ranked_jobs[0]

#     print()

#     print("=" * 80)
#     print("Generating Interview Plan...")
#     print("=" * 80)

#     planner = InterviewPlannerService()

#     interview_plan = planner.generate_plan(
#         profile=profile,
#         job=selected_job,
#         interview_mode=InterviewMode.MIXED,
#         difficulty=DifficultyLevel.MEDIUM,
#     )

#     print()

#     print("=" * 80)
#     print("Interview Plan")
#     print("=" * 80)

#     pprint(
#         interview_plan.model_dump(),
#         sort_dicts=False,
#     )


# if __name__ == "__main__":
#     main() 

# from pprint import pprint

# from backend.graphs.workflow import graph

# from backend.Interview.services.interview_planner_service import (
#     InterviewPlannerService,
# )

# from backend.Interview.services.question_generation_service import (
#     QuestionGenerationService,
# )

# from backend.Interview.schemas.interview_plan import (
#     InterviewMode,
#     DifficultyLevel,
# )

# from backend.Interview.schemas.interview_question import (
#     QuestionCategory,
# )

# RESUME_PATH = "/Users/ashutoshkushwaha/Desktop/Ashutosh_resume.pdf"


# def main():

#     # ----------------------------------------------------
#     # Resume + Job Pipeline
#     # ----------------------------------------------------

#     state = {
#         "messages": [],
#         "resume_path": RESUME_PATH,
#     }

#     print("=" * 80)
#     print("Running Resume + Job Graph...")
#     print("=" * 80)

#     state = graph.invoke(state)

#     profile = state["candidate_profile"]

#     ranked_jobs = state["ranked_jobs"]

#     if not ranked_jobs:
#         raise ValueError("No jobs found.")

#     selected_job = ranked_jobs[0]

#     # ----------------------------------------------------
#     # Interview Planner
#     # ----------------------------------------------------

#     planner = InterviewPlannerService()

#     interview_plan = planner.generate_plan(
#         profile=profile,
#         job=selected_job,
#         interview_mode=InterviewMode.MIXED,
#         difficulty=DifficultyLevel.MEDIUM,
#     )

#     # ----------------------------------------------------
#     # Question Generator
#     # ----------------------------------------------------

#     question_service = QuestionGenerationService()

#     question = question_service.generate_question(
#         profile=profile,
#         job=selected_job,
#         interview_plan=interview_plan,
#         question_number=1,
#         category=QuestionCategory.TECHNICAL,
#         previous_questions=[],
#     )

#     print()
#     print("=" * 80)
#     print("Generated Interview Question")
#     print("=" * 80)

#     pprint(
#         question.model_dump(),
#         sort_dicts=False,
#     )


# if __name__ == "__main__":
#     main()


from pprint import pprint
from datetime import datetime

from backend.graphs.workflow import graph

from backend.Interview.services.interview_planner_service import (
    InterviewPlannerService,
)

from backend.Interview.services.question_generation_service import (
    QuestionGenerationService,
)

from backend.Interview.services.answer_evaluation_service import (
    AnswerEvaluationService,
)

from backend.Interview.services.interview_report_service import (
    InterviewReportService,
)

from backend.Interview.schemas.interview_plan import (
    InterviewMode,
    DifficultyLevel,
)

from backend.Interview.schemas.interview_question import (
    QuestionCategory,
)

from backend.Interview.schemas.interview_answer import (
    InterviewAnswer,
    AnswerSource,
)

from backend.Interview.schemas.interview_session import (
    InterviewSession,
    InterviewStatus,
)

from backend.Interview.schemas.question_answer_pair import (
    QuestionAnswerPair,
)

RESUME_PATH = "/Users/ashutoshkushwaha/Desktop/Ashutosh_resume.pdf"


def sample_answer(question: str) -> str:
    """
    Returns a realistic sample answer.
    """

    return """
In WanderNest I implemented authentication using JWT.

When a user logs in, the backend verifies the user's
credentials using bcrypt to compare the hashed password.

If authentication succeeds, a JWT token is generated
and returned to the frontend.

Protected routes use middleware that validates the JWT
before allowing access.

Passwords are never stored in plain text.

If I were improving the project further,
I would add refresh tokens,
role-based authorization,
and HTTP-only cookies.
"""


def main():

    # =====================================================
    # Resume + Jobs
    # =====================================================

    print("=" * 80)
    print("Resume + Job Pipeline")
    print("=" * 80)

    state = graph.invoke(
        {
            "messages": [],
            "resume_path": RESUME_PATH,
        }
    )

    profile = state["candidate_profile"]
    selected_job = state["ranked_jobs"][0]

    # =====================================================
    # Planner
    # =====================================================

    planner = InterviewPlannerService()

    plan = planner.generate_plan(
        profile=profile,
        job=selected_job,
        interview_mode=InterviewMode.MIXED,
        difficulty=DifficultyLevel.MEDIUM,
    )

    print()
    print("=" * 80)
    print("Interview Plan")
    print("=" * 80)

    pprint(plan.model_dump(), sort_dicts=False)

    # =====================================================
    # Session
    # =====================================================

    session = InterviewSession(
        candidate=profile,
        target_job=selected_job,
        interview_plan=plan,
        status=InterviewStatus.IN_PROGRESS,
        started_at=datetime.utcnow(),
    )

    question_service = QuestionGenerationService()
    evaluation_service = AnswerEvaluationService()

    previous_questions = []

    TOTAL_QUESTIONS = 3

    categories = [
        QuestionCategory.TECHNICAL,
        QuestionCategory.PROJECT,
        QuestionCategory.BEHAVIORAL,
    ]

    # =====================================================
    # Interview Loop
    # =====================================================

    for index in range(TOTAL_QUESTIONS):

        print()
        print("=" * 80)
        print(f"Question {index+1}")
        print("=" * 80)

        question = question_service.generate_question(
            profile=profile,
            job=selected_job,
            interview_plan=plan,
            question_number=index + 1,
            category=categories[index],
            previous_questions=previous_questions,
        )

        previous_questions.append(question.question)

        print(question.question)

        answer = InterviewAnswer(
            question_id=question.question_id,
            transcript=sample_answer(question.question),
            source=AnswerSource.TEXT,
            duration_seconds=90,
        )

        feedback = evaluation_service.evaluate(
            profile=profile,
            job=selected_job,
            question=question,
            answer=answer,
        )

        pair = QuestionAnswerPair(
            question=question,
            answer=answer,
            feedback=feedback,
            interaction_completed=True,
        )

        session.history.append(pair)

        print()
        print("Overall Score:", feedback.overall.score)

    # =====================================================
    # Finish Session
    # =====================================================

    session.status = InterviewStatus.COMPLETED
    session.ended_at = datetime.utcnow()

    # =====================================================
    # Report
    # =====================================================

    report_service = InterviewReportService()

    report = report_service.generate_report(session)

    print()
    print("=" * 80)
    print("FINAL REPORT")
    print("=" * 80)

    pprint(report.model_dump(), sort_dicts=False)


if __name__ == "__main__":
    main()
