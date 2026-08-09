from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

"""
    Structured representation of a candidate extracted from a resume.
    This schema is shared across multiple agents including:
    - Resume Agent
    - Job Matching Agent
    - Recruiter Agent
    - Interview Agent
    """

class Experience(BaseModel):
    company: str
    role: str
    duration: Optional[str] = None
    description: Optional[str] = None


class Project(BaseModel):
    title: str
    technologies: List[str] = Field(default_factory=list)
    description: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    year: Optional[str] = None


class CandidateProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    linkedin: Optional[str] = None
    github: Optional[str] = None
    #strengths: List[str] = Field(default_factory=list)
    #weaknesses: List[str] = Field(default_factory=list)