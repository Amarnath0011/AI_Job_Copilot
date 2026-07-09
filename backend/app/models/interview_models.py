from typing import List

from pydantic import BaseModel, Field


class InterviewQuestionRequest(BaseModel):
    job_description: str = Field(
        ...,
        min_length=50,
        description="Job description used to generate personalized interview questions.",
    )


class InterviewQuestionResponse(BaseModel):
    """
    Structured response returned by the Interview Question Generator.
    """

    technical: List[str] = Field(
        description="List of personalized technical interview questions."
    )

    behavioral: List[str] = Field(
        description="List of behavioral interview questions."
    )

    hr: List[str] = Field(
        description="List of HR interview questions."
    )