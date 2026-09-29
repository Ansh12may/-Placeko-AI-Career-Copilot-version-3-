from pydantic import BaseModel, HttpUrl,Field
from typing import List, Optional
from backend.Jobs.schemas.job_readiness import JobReadiness

class Job(BaseModel):
    """
    Represents a single job posting.
    """
    job_id: Optional[str] = None
    title: str
    company: str
    location: str
    employment_type: Optional[str] = None
    experience: Optional[str] = None
    salary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    description: str
    apply_url: Optional[HttpUrl] = None
    source: str
    pinecone_score: float | None = None
    reranker_score: float | None = None
    job_readiness: JobReadiness | None = None
   