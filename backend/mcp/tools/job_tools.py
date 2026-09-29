"""
Placeko MCP Tools

Thin MCP adapters around existing Placeko business services.

MCP exposes capabilities.
Existing Placeko services remain responsible for business logic.
"""

from typing import Any

from backend.mcp.server import mcp

from backend.Jobs.tools.job_search_tool import JobSearchTool
from backend.Jobs.repositories.job_repository import JobRepository
from backend.Jobs.services.job_readiness_service import (
    JobReadinessService,
)

from backend.Resume.repositories.resume_repository import (
    ResumeRepository,
)
from backend.Resume.schemas.candidate import CandidateProfile


# ============================================================
# EXISTING PLACEKO SERVICES
# ============================================================

job_search_tool = JobSearchTool()
job_repository = JobRepository()
resume_repository = ResumeRepository()
job_readiness_service = JobReadinessService()


# ============================================================
# HELPERS
# ============================================================

def _load_candidate_profile(
    resume: dict[str, Any],
) -> CandidateProfile | None:
    """
    Convert stored candidate_profile data into the
    existing CandidateProfile schema.
    """

    candidate_profile_data = resume.get("candidate_profile")

    if not candidate_profile_data:
        return None

    try:
        return CandidateProfile.model_validate(
            candidate_profile_data
        )
    except Exception:
        return None


def _normalise_text(value: str) -> str:
    """
    Normalise text for deterministic matching.
    """

    return " ".join(
        value.lower().strip().split()
    )


def _requirement_matches(
    requirement: str,
    searchable_text: str,
) -> bool:
    """
    Match a requirement against grounded resume text.

    Supports:
    - exact phrases
    - individual words
    - common technology aliases
    """

    requirement_normalised = _normalise_text(
        requirement
    )

    searchable_normalised = _normalise_text(
        searchable_text
    )

    if not requirement_normalised:
        return False

    # Exact phrase match
    if requirement_normalised in searchable_normalised:
        return True

    # Technology aliases
    aliases = {
        "llm": [
            "llm",
            "large language model",
            "large language models",
            "generative ai",
            "genai",
        ],
        "rag": [
            "rag",
            "retrieval augmented generation",
            "retrieval-augmented generation",
        ],
        "langgraph": [
            "langgraph",
        ],
        "langchain": [
            "langchain",
        ],
        "fastapi": [
            "fastapi",
        ],
        "python": [
            "python",
        ],
        "pytorch": [
            "pytorch",
        ],
        "machine learning": [
            "machine learning",
            "ml",
        ],
        "deep learning": [
            "deep learning",
            "dl",
        ],
        "nlp": [
            "nlp",
            "natural language processing",
        ],
        "vector database": [
            "vector database",
            "vector db",
            "pinecone",
            "faiss",
        ],
        "pinecone": [
            "pinecone",
        ],
        "docker": [
            "docker",
        ],
        "aws": [
            "aws",
            "amazon web services",
        ],
    }

    requirement_aliases = aliases.get(
        requirement_normalised,
        [requirement_normalised],
    )

    return any(
        alias in searchable_normalised
        for alias in requirement_aliases
    )


def _build_grounded_evidence(
    profile: CandidateProfile,
    query: str,
) -> dict[str, Any]:
    """
    Search only grounded CandidateProfile fields.

    No free-form inference is performed here.
    """

    query_normalised = _normalise_text(query)

    # --------------------------------------------------------
    # Build searchable candidate evidence
    # --------------------------------------------------------

    grounded_skills: list[str] = []
    grounded_projects: list[dict[str, Any]] = []
    grounded_experience: list[dict[str, Any]] = []

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    for skill in profile.skills:
        if _requirement_matches(
            skill,
            query_normalised,
        ):
            grounded_skills.append(skill)

    # --------------------------------------------------------
    # PROJECTS
    # --------------------------------------------------------

    for project in profile.projects:

        matched_technologies: list[str] = []

        for technology in project.technologies:

            if _requirement_matches(
                technology,
                query_normalised,
            ):
                matched_technologies.append(
                    technology
                )

        # Also check project title
        title_match = _requirement_matches(
            project.title,
            query_normalised,
        )

        if matched_technologies or title_match:

            grounded_projects.append(
                {
                    "title": project.title,
                    "technologies": (
                        matched_technologies
                    ),
                    "description": project.description,
                }
            )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    for experience in profile.experience:

        searchable_text = " ".join(
            [
                experience.company or "",
                experience.role or "",
                experience.description or "",
            ]
        )

        if _requirement_matches(
            searchable_text,
            query_normalised,
        ):

            grounded_experience.append(
                {
                    "company": experience.company,
                    "role": experience.role,
                    "duration": experience.duration,
                    "description": experience.description,
                }
            )

    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    evidence: list[dict[str, Any]] = []

    for skill in grounded_skills:

        evidence.append(
            {
                "source_type": "skill",
                "source": skill,
                "matched_text": skill,
            }
        )

    for project in grounded_projects:

        technologies = project["technologies"]

        matched_text = ", ".join(
            technologies
        )

        if not matched_text:
            matched_text = project["title"]

        evidence.append(
            {
                "source_type": "project",
                "source": project["title"],
                "matched_text": matched_text,
            }
        )

    for experience in grounded_experience:

        evidence.append(
            {
                "source_type": "experience",
                "source": (
                    f"{experience['role']} "
                    f"at {experience['company']}"
                ),
                "matched_text": (
                    experience["description"]
                ),
            }
        )

    return {
        "found": bool(evidence),
        "query": query,
        "evidence": evidence,
        "grounded_skills": grounded_skills,
        "grounded_projects": grounded_projects,
        "grounded_experience": grounded_experience,
    }


# ============================================================
# SEARCH JOBS
# ============================================================

@mcp.tool()
def search_jobs(
    query: str,
    country: str = "in",
    page: int = 1,
) -> list[dict[str, Any]]:
    """
    Search fresh job postings using Placeko's
    existing JSearch integration.
    """

    jobs = job_search_tool.search_jobs(
        query=query,
        country=country,
        page=page,
    )

    return [
        job.model_dump(mode="json")
        for job in jobs
    ]


# ============================================================
# GET JOB DETAILS
# ============================================================

@mcp.tool()
async def get_job_details(
    user_id: str,
    resume_id: str,
    job_id: str,
) -> dict[str, Any]:
    """
    Retrieve a persisted Placeko job recommendation.
    """

    job = await job_repository.get_job(
        user_id=user_id,
        resume_id=resume_id,
        job_id=job_id,
    )

    if job is None:

        return {
            "found": False,
            "job_id": job_id,
            "message": "Job not found.",
        }

    return {
        "found": True,
        "job": job.model_dump(
            mode="json"
        ),
    }


# ============================================================
# SEARCH RESUME EVIDENCE
# ============================================================

@mcp.tool()
async def search_resume_evidence(
    user_id: str,
    query: str,
    resume_id: str | None = None,
) -> dict[str, Any]:
    """
    Search the candidate's stored resume profile for
    grounded evidence relevant to a query.

    Evidence comes only from the stored CandidateProfile.
    """

    # --------------------------------------------------------
    # Resolve active resume
    # --------------------------------------------------------

    if resume_id is None:

        resume = await resume_repository.get_active_resume(
            user_id=user_id
        )

        if resume is None:

            return {
                "found": False,
                "message": "No active resume found.",
            }

        resume_id = resume.get("id")

    # --------------------------------------------------------
    # Load resume
    # --------------------------------------------------------

    resume = await resume_repository.get_resume_by_id(
        resume_id=resume_id,
        user_id=user_id,
    )

    if resume is None:

        return {
            "found": False,
            "resume_id": resume_id,
            "message": "Resume not found.",
        }

    # --------------------------------------------------------
    # Load candidate profile
    # --------------------------------------------------------

    profile = _load_candidate_profile(
        resume
    )

    if profile is None:

        return {
            "found": False,
            "resume_id": resume_id,
            "message": (
                "Candidate profile is unavailable "
                "or invalid."
            ),
        }

    # --------------------------------------------------------
    # Search grounded evidence
    # --------------------------------------------------------

    result = _build_grounded_evidence(
        profile=profile,
        query=query,
    )

    return {
        "found": result["found"],
        "resume_id": resume_id,
        "query": query,
        "evidence": result["evidence"],
        "grounded_skills": result[
            "grounded_skills"
        ],
        "grounded_projects": result[
            "grounded_projects"
        ],
        "grounded_experience": result[
            "grounded_experience"
        ],
        "grounded_skill_count": len(
            profile.skills
        ),
        "grounded_project_count": len(
            profile.projects
        ),
        "source_verification": {
            "verified": True,
            "source": "stored_candidate_profile",
        },
    }


# ============================================================
# ANALYZE PERSISTED JOB READINESS
# ============================================================

@mcp.tool()
async def analyze_job_readiness(
    user_id: str,
    resume_id: str,
    job_id: str,
) -> dict[str, Any]:
    """
    Analyze candidate readiness against a persisted job.
    """

    job = await job_repository.get_job(
        user_id=user_id,
        resume_id=resume_id,
        job_id=job_id,
    )

    if job is None:

        return {
            "found": False,
            "job_id": job_id,
            "message": "Job not found.",
        }

    resume = await resume_repository.get_resume_by_id(
        resume_id=resume_id,
        user_id=user_id,
    )

    if resume is None:

        return {
            "found": False,
            "resume_id": resume_id,
            "message": "Resume not found.",
        }

    profile = _load_candidate_profile(
        resume
    )

    if profile is None:

        return {
            "found": False,
            "resume_id": resume_id,
            "message": (
                "Candidate profile is unavailable "
                "or invalid."
            ),
        }

    analyzed_job = (
        await job_readiness_service.analyze_job(
            profile=profile,
            job=job,
            user_id=user_id,
            resume_id=resume_id,
        )
    )

    return {
        "found": True,
        "job_id": job_id,
        "readiness": (
            analyzed_job.job_readiness.model_dump(
                mode="json"
            )
            if analyzed_job.job_readiness
            else None
        ),
    }


# ============================================================
# ANALYZE FRESH JOB READINESS
# ============================================================

@mcp.tool()
async def analyze_fresh_job_readiness(
    user_id: str,
    resume_id: str,
    job: dict[str, Any],
) -> dict[str, Any]:
    """
    Analyze readiness against a fresh job returned directly
    by search_jobs.

    This does NOT require the job to already exist in MongoDB.
    """

    # --------------------------------------------------------
    # Load resume
    # --------------------------------------------------------

    resume = await resume_repository.get_resume_by_id(
        resume_id=resume_id,
        user_id=user_id,
    )

    if resume is None:

        return {
            "found": False,
            "resume_id": resume_id,
            "message": "Resume not found.",
        }

    # --------------------------------------------------------
    # Load candidate profile
    # --------------------------------------------------------

    profile = _load_candidate_profile(
        resume
    )

    if profile is None:

        return {
            "found": False,
            "resume_id": resume_id,
            "message": (
                "Candidate profile is unavailable "
                "or invalid."
            ),
        }

    # --------------------------------------------------------
    # Validate fresh job
    # --------------------------------------------------------

    try:

        from backend.Jobs.schemas.job import Job

        fresh_job = Job.model_validate(job)

    except Exception as error:

        return {
            "found": False,
            "resume_id": resume_id,
            "message": "Invalid job payload.",
            "error": str(error),
        }

    # --------------------------------------------------------
    # Existing business service
    # --------------------------------------------------------

    analyzed_job = (
        await job_readiness_service.analyze_job(
            profile=profile,
            job=fresh_job,
            user_id=user_id,
            resume_id=resume_id,
        )
    )

    # --------------------------------------------------------
    # Return grounded result
    # --------------------------------------------------------

    return {
        "found": True,
        "job_id": fresh_job.job_id,
        "job": fresh_job.model_dump(
            mode="json"
        ),
        "readiness": (
            analyzed_job.job_readiness.model_dump(
                mode="json"
            )
            if analyzed_job.job_readiness
            else None
        ),
    }

# ============================================================
# GET RECOMMENDED JOBS
# ============================================================

@mcp.tool()
async def get_recommended_jobs(
    user_id: str,
    resume_id: str,
) -> dict[str, Any]:
    """
    Retrieve the user's already-generated job recommendations.

    This does NOT perform job searching, ranking, or LLM reasoning.
    It only reads the persisted recommendation snapshot.
    """

    jobs = await job_repository.get_recommendations(
        user_id=user_id,
        resume_id=resume_id,
    )

    if not jobs:
        return {
            "found": False,
            "resume_id": resume_id,
            "jobs": [],
            "message": "No persisted job recommendations found.",
        }

    return {
        "found": True,
        "resume_id": resume_id,
        "jobs": [
            job.model_dump(mode="json")
            for job in jobs
        ],
        "count": len(jobs),
        "source": "persisted_recommendations",
    }