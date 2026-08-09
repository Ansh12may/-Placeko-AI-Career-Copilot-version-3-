"""
Text Formatter Utility
Converts structured schema objects into rich text
representations suitable for embedding generation.

Embeddings work on text, not Python objects.
The quality of retrieval depends heavily on how
well we represent the resume and job posting.
"""

from backend.Resume.schemas.candidate import CandidateProfile
from backend.Jobs.schemas.job import Job


def resume_to_text(profile: CandidateProfile) -> str:
    education = "\n".join(
        [
            f"{edu.degree} at {edu.institution} ({edu.year})"
            for edu in profile.education
        ]
    )
    experience = "\n".join(
        [
            f"{exp.role} at {exp.company}\n{exp.description or ''}"
            for exp in profile.experience
        ]
    )
    projects = "\n".join(
        [
            f"{project.title}\n"
            f"Technologies: {', '.join(project.technologies)}\n"
            f"{project.description}"
            for project in profile.projects
        ]
    )
    certifications = "\n".join(profile.certifications or [])
    skills = ", ".join(profile.skills)
    return f"""
Candidate Name:
{profile.name}

Skills:
{skills}

Education:
{education}

Experience:
{experience}

Projects:
{projects}

Certifications:
{certifications}
""".strip()


def job_to_text(job: Job) -> str:
   
    skills = ", ".join(job.skills or [])

    return f"""
Job Title:
{job.title}

Company:
{job.company}

Location:
{job.location}

Employment Type:
{job.employment_type}

Required Skills:
{skills}

Job Description:
{job.description}
""".strip()