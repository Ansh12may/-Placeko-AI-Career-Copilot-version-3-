"""
LLM Formatter Utility

Converts structured schema objects into a rich,
human-readable text representation for Large
Language Model reasoning.

Unlike embedding formatters, this formatter
preserves section labels and contextual information
to improve LLM understanding.
"""

from backend.Resume.schemas.candidate import CandidateProfile


def resume_to_llm_text(profile: CandidateProfile) -> str:
    """
    Convert a CandidateProfile into a structured
    text format optimized for LLM analysis.
    """

    education = "\n".join(
        [
            (
                f"- Degree: {edu.degree}\n"
                f"  Institution: {edu.institution}\n"
                f"  Year: {edu.year or 'Not Provided'}"
            )
            for edu in profile.education
        ]
    )

    experience = "\n".join(
        [
            (
                f"- Role: {exp.role}\n"
                f"  Company: {exp.company}\n"
                f"  Duration: {exp.duration or 'Not Provided'}\n"
                f"  Description: {exp.description or 'Not Provided'}"
            )
            for exp in profile.experience
        ]
    )

    projects = "\n".join(
        [
            (
                f"- Title: {project.title}\n"
                f"  Technologies: {', '.join(project.technologies) if project.technologies else 'Not Provided'}\n"
                f"  Description: {project.description or 'Not Provided'}"
            )
            for project in profile.projects
        ]
    )

    certifications = (
        "\n".join(f"- {cert}" for cert in profile.certifications)
        if profile.certifications
        else "Not Provided"
    )

    skills = (
        ", ".join(profile.skills)
        if profile.skills
        else "Not Provided"
    )

    linkedin = getattr(profile, "linkedin", None)
    github = getattr(profile, "github", None)

    return f"""
==============================
CANDIDATE PROFILE
==============================

Name:
{profile.name or "Not Provided"}

Email:
{profile.email or "Not Provided"}

Phone:
{profile.phone or "Not Provided"}

LinkedIn:
{linkedin or "Not Provided"}

GitHub:
{github or "Not Provided"}

Professional Summary:
{profile.summary or "Not Provided"}

Skills:
{skills}

Education:
{education or "Not Provided"}

Experience:
{experience or "Not Provided"}

Projects:
{projects or "Not Provided"}

Certifications:
{certifications}
""".strip()