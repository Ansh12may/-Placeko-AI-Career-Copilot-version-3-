from pydantic import BaseModel
from backend.Jobs.schemas.job import Job

class ApplicationWorkflowStartRequest(BaseModel):
    """
    Request for starting an agentic application workflow.
    """
    job: Job