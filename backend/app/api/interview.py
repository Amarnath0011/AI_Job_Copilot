from fastapi import APIRouter, HTTPException

from app.models.interview_models import (
    InterviewAnswerRequest,
    InterviewEndRequest,
    InterviewEvaluationRequest,
    InterviewQuestionRequest,
    InterviewStartRequest,
)
from app.services.interview_service import interview_service

router = APIRouter(
    prefix="/interview",
    tags=["AI Interview Coach"],
)


# ==========================================================
# Feature 5.1
# ==========================================================

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


# ==========================================================
# Feature 5.2
# ==========================================================

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


# ==========================================================
# Feature 5.3
# ==========================================================

@router.post("/start")
def start_interview(
    request: InterviewStartRequest,
):
    """
    Start a new adaptive interview session.
    """

    try:

        result = interview_service.start_interview(request)

        return {
            "success": True,
            "message": "Interview started successfully.",
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
            detail=f"Unable to start interview: {str(e)}",
        )


@router.post("/answer")
def submit_answer(
    request: InterviewAnswerRequest,
):
    """
    Submit an answer for the current interview question.
    """

    try:

        result = interview_service.submit_answer(request)

        return {
            "success": True,
            "message": "Answer evaluated successfully.",
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
            detail=f"Unable to evaluate answer: {str(e)}",
        )


@router.post("/end")
def end_interview(
    request: InterviewEndRequest,
):
    """
    End the interview session and generate the final report.
    """

    try:

        result = interview_service.end_interview(request)

        return {
            "success": True,
            "message": "Interview completed successfully.",
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
            detail=f"Unable to generate interview report: {str(e)}",
        )
        
# @router.post("/report")
