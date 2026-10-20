from pydantic import BaseModel, Field


class ATSRequest(BaseModel):
    session_id: str = Field(..., description="Resume session ID returned after upload.")
    job_description: str = Field(..., min_length=20, description="Job description to compare with the uploaded resume.")
