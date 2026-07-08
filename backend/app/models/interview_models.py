from pydantic import BaseModel, Field
from typing import List


class InterviewQuestionRequest(BaseModel):
    job_description: str = Field(
        ...,
        min_length=50,
        description="Job description used to generate personalized interview questions."
    )


class InterviewQuestionResponse(BaseModel):
    technical: List[str] = Field(
        default_factory=list,
        description="List of technical interview questions."
    )

    behavioral: List[str] = Field(
        default_factory=list,
        description="List of behavioral interview questions."
    )

    hr: List[str] = Field(
        default_factory=list,
        description="List of HR interview questions."
    )