from pydantic import BaseModel, HttpUrl,Field
from typing import List, Optional

class Job(BaseModel):
    """
    Represents a single job posting.
    """
    title: str
    company: str
    location: str
    employment_type: Optional[str] = None
    experience: Optional[str] = None
    salary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    description: str
    apply_url: HttpUrl
    source: str