from typing import List

from pydantic import BaseModel, Field


# ==========================================================
# Interview Question Generation
# ==========================================================

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


# ==========================================================
# Interview Answer Evaluation
# ==========================================================

class InterviewEvaluationRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=10,
        description="Interview question asked to the candidate."
    )

    answer: str = Field(
        ...,
        min_length=10,
        description="Candidate's answer."
    )


class InterviewEvaluationResponse(BaseModel):
    """
    Structured response returned by the Interview Evaluator.
    """

    overall_score: int = Field(
        description="Overall interview score out of 100."
    )

    technical_score: int = Field(
        description="Technical correctness score out of 100."
    )

    communication_score: int = Field(
        description="Communication quality score out of 100."
    )

    feedback: str = Field(
        description="Overall feedback for the candidate."
    )

    strengths: List[str] = Field(
        description="Strengths identified in the answer."
    )

    improvements: List[str] = Field(
        description="Suggestions to improve the answer."
    )

    expected_answer: str = Field(
        description="An ideal answer expected from the candidate."
    )