from pydantic import BaseModel, Field


class ATSRequest(BaseModel):
    
    session_id: str = Field(
        ...,
        description="Session ID returned after resume upload."
    )

    job_description: str = Field(
        ...,
        min_length=20,
    )