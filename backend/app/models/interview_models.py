from typing import List, Optional

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
        description="Ideal answer expected from the candidate."
    )


# ==========================================================
# Interview Session Engine
# ==========================================================

class InterviewStartRequest(BaseModel):
    """
    Starts a new interview session.
    """

    job_description: str = Field(
        ...,
        min_length=50,
        description="Job description for interview preparation."
    )


class InterviewStartResponse(BaseModel):
    """
    Returned after successfully starting an interview.
    """

    session_id: str

    question_number: int

    total_questions: int

    question: str


class InterviewAnswerRequest(BaseModel):
    """
    Candidate submits an answer.
    """

    session_id: str

    answer: str = Field(
        ...,
        min_length=2,
        description="Candidate's answer."
    )


class InterviewHistoryItem(BaseModel):
    """
    One completed interview interaction.
    """

    question: str

    answer: str

    evaluation: InterviewEvaluationResponse


class InterviewAnswerResponse(BaseModel):
    """
    Returned after evaluating an answer.
    """

    evaluation: InterviewEvaluationResponse

    question_number: int

    total_questions: int

    interview_completed: bool

    next_question: Optional[str] = None


class InterviewEndRequest(BaseModel):
    """
    Ends an interview session.
    """

    session_id: str

class QuestionFeedback(BaseModel):
    """
    Feedback for an individual interview question.
    """

    question: str

    score: int = Field(..., ge=0, le=100)

    feedback: str

    ideal_answer_summary: str


class InterviewReportResponse(BaseModel):
    """
    Final interview report generated after the interview session.
    """

    overall_score: int = Field(..., ge=0, le=100)

    technical_score: int = Field(..., ge=0, le=100)

    communication_score: int = Field(..., ge=0, le=100)

    problem_solving_score: int = Field(..., ge=0, le=100)

    confidence_score: int = Field(..., ge=0, le=100)

    strengths: List[str]

    weaknesses: List[str]

    knowledge_gaps: List[str]

    question_feedback: List[QuestionFeedback]

    learning_roadmap: List[str]

    difficulty_level: str

    hiring_recommendation: str

    summary: str