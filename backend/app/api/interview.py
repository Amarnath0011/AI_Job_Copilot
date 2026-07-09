from fastapi import APIRouter, HTTPException

from app.models.interview_models import (
    InterviewEvaluationRequest,
    InterviewQuestionRequest,
)
from app.services.interview_service import interview_service

router = APIRouter(
    prefix="/interview",
    tags=["AI Interview Coach"],
)


@router.post("/questions")
def generate_interview_questions(
    request: InterviewQuestionRequest,
):
    """
    Generate personalized interview questions using:
    - Uploaded Resume (RAG)
    - Job Description
    """

    try:
        result = interview_service.generate_questions(request)

        return {
            "success": True,
            "message": "Interview questions generated successfully.",
            "data": result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Interview generation failed: {str(e)}",
        )


@router.post("/evaluate")
def evaluate_answer(
    request: InterviewEvaluationRequest,
):
    """
    Evaluate a candidate's interview answer.
    """

    try:
        result = interview_service.evaluate_answer(request)

        return {
            "success": True,
            "message": "Interview answer evaluated successfully.",
            "data": result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Interview evaluation failed: {str(e)}",
        )