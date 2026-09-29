"""
Job Readiness & Gap Evidence Service

Purpose:
    Requirement Extraction
        -> Candidate Evidence Mapping
        -> Proven / Unproven / Resume Gap
        -> Human confirmation support

This service is deterministic. It does not use an LLM to invent
candidate skills or to decide that a candidate knows a technology.
It only maps explicit job requirements to evidence already present
in the CandidateProfile, plus explicit candidate confirmations.
"""

import hashlib
import re
from typing import Iterable, List

from backend.Jobs.schemas.job import Job
from backend.Jobs.schemas.job_readiness import (
    CandidateEvidence,
    JobReadiness,
    JobRequirementEvidence,
)
from backend.Jobs.repositories.readiness_repository import ReadinessRepository
from backend.Resume.schemas.candidate import CandidateProfile


class JobReadinessService:
    """Build explainable job requirement-to-evidence mappings."""

    # Curated technical vocabulary. Keeping this deterministic makes
    # requirement extraction auditable and easy to defend in interviews.
    REQUIREMENT_CATALOG = [
        "python", "java", "c++", "c#", "javascript", "typescript", "go", "rust",
        "fastapi", "django", "flask", "react", "next.js", "node.js", "express",
        "spring boot", "rest api", "rest apis", "graphql", "microservices",
        "mongodb", "mysql", "postgresql", "sql", "redis", "pinecone",
        "machine learning", "deep learning", "nlp", "llm", "generative ai",
        "langchain", "langgraph", "rag", "embeddings", "pytorch", "tensorflow",
        "scikit-learn", "lightgbm", "docker", "kubernetes", "aws", "azure", "gcp",
        "github", "git", "ci/cd", "mlops", "airflow", "spark", "pandas", "numpy",
        "jwt", "oauth", "linux", "bash", "terraform", "jenkins", "postman",
    ]

    def __init__(self):
        self.repository = ReadinessRepository()

    @staticmethod
    def job_key(job: Job) -> str:
        raw = "|".join(
            [
                job.job_id or "",
                job.title.strip().lower(),
                job.company.strip().lower(),
                job.location.strip().lower(),
            ]
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text.lower()).strip()

    def extract_requirements(self, job: Job) -> List[str]:
        """Extract explicit technical requirements from skills and description."""
        candidates = list(job.skills or [])
        description = self._normalize(job.description or "")

        # Add catalog items found in the job description. Word boundaries
        # prevent accidental matches such as `go` inside `good`.
        for requirement in self.REQUIREMENT_CATALOG:
            pattern = re.escape(requirement)
            if re.search(rf"(?<![a-z0-9+#]){pattern}(?![a-z0-9+#])", description):
                candidates.append(requirement)

        result: List[str] = []
        seen = set()
        for item in candidates:
            value = re.sub(r"\s+", " ", str(item).strip())
            if not value:
                continue
            key = value.lower()
            if key not in seen:
                seen.add(key)
                result.append(value)

        return result

    def _candidate_evidence(
        self,
        profile: CandidateProfile,
        requirement: str,
    ) -> List[CandidateEvidence]:
        target = self._normalize(requirement)
        evidence: List[CandidateEvidence] = []

        def matches(value: str | None) -> bool:
            if not value:
                return False
            normalized = self._normalize(value)
            # Exact-ish phrase matching for multi-word technologies and
            # token matching for short names such as C++ / Go.
            if target in normalized:
                return True
            return False

        for skill in profile.skills:
            if matches(skill):
                evidence.append(
                    CandidateEvidence(
                        source_type="skill",
                        source="Technical skills",
                        matched_text=skill,
                    )
                )

        # The downstream profile is source-grounded. Therefore project
        # evidence is limited to grounded project technologies rather than
        # using free-form project descriptions as proof. Experience and
        # certifications are intentionally not treated as technical proof
        # until they have their own grounding rules.
        for project in profile.projects:
            for technology in project.technologies:
                if matches(technology):
                    evidence.append(
                        CandidateEvidence(
                            source_type="project",
                            source=project.title,
                            matched_text=technology,
                        )
                    )

        return evidence

    async def analyze_job(
        self,
        profile: CandidateProfile,
        job: Job,
        user_id: str,
        resume_id: str,
    ) -> Job:
        # Keep the UI focused on the most useful technical requirements.
        requirements = self.extract_requirements(job)[:15]
        confirmations = {
            item.lower()
            for item in await self.repository.get_confirmations(
                user_id=user_id,
                resume_id=resume_id,
                job_key=self.job_key(job),
            )
        }

        mapped: List[JobRequirementEvidence] = []
        counts = {
            "proven": 0,
            "unproven": 0,
            "resume_gap": 0,
            "candidate_confirmed": 0,
        }

        for requirement in requirements:
            evidence = self._candidate_evidence(profile, requirement)
            key = requirement.lower()

            if key in confirmations:
                status = "candidate_confirmed"
                explanation = (
                    "Candidate confirmed this requirement, but the current resume "
                    "does not provide direct evidence for it."
                )
                evidence = [
                    CandidateEvidence(
                        source_type="candidate_confirmation",
                        source="Candidate verification",
                        matched_text=requirement,
                    )
                ]
            elif evidence:
                contextual_evidence = any(
                    item.source_type in {"project", "experience", "certification"}
                    for item in evidence
                )
                if contextual_evidence:
                    status = "proven"
                    explanation = (
                        "The grounded candidate profile contains contextual evidence "
                        "in a project, experience entry, or certification."
                    )
                else:
                    status = "unproven"
                    explanation = (
                        "The skill is listed in the resume, but the current profile "
                        "does not provide stronger contextual evidence."
                    )
            else:
                status = "resume_gap"
                explanation = (
                    "The job explicitly requires this capability, but the current "
                    "resume/profile does not provide supporting evidence. This does "
                    "not mean the candidate lacks the skill."
                )

            counts[status] += 1
            mapped.append(
                JobRequirementEvidence(
                    requirement=requirement,
                    status=status,
                    evidence=evidence,
                    explanation=explanation,
                )
            )

        job.job_readiness = JobReadiness(
            requirements=mapped,
            proven_count=counts["proven"],
            unproven_count=counts["unproven"],
            resume_gap_count=counts["resume_gap"],
            candidate_confirmed_count=counts["candidate_confirmed"],
        )
        return job

    async def analyze_jobs(
        self,
        profile: CandidateProfile,
        jobs: Iterable[Job],
        user_id: str,
        resume_id: str,
    ) -> List[Job]:
        result = []
        for job in jobs:
            result.append(
                await self.analyze_job(
                    profile=profile,
                    job=job,
                    user_id=user_id,
                    resume_id=resume_id,
                )
            )
        return result

    async def confirm_requirement(
        self,
        user_id: str,
        resume_id: str,
        job: Job,
        requirement: str,
    ) -> None:
        await self.repository.confirm_requirement(
            user_id=user_id,
            resume_id=resume_id,
            job_key=self.job_key(job),
            requirement=requirement.strip(),
        )
