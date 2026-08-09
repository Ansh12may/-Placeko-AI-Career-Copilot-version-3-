from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from backend.Resume.schemas.candidate import CandidateProfile
from backend.ATS.schemas.ats_report import ATSReport


class ResumeResponse(BaseModel):
    id: str
    user_id: str
    file_name: str
    file_size: int
    content_type: Optional[str] = None
    candidate_profile: CandidateProfile
    ats_report: Optional[ATSReport] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ResumeListItem(BaseModel):
    id: str
    file_name: str
    file_size: int
    content_type: Optional[str] = None
    candidate_name: Optional[str] = None
    ats_score: Optional[float] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime