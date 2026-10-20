from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.db.models import User
from app.models.interview_models import (
    InterviewAnswerRequest,
    InterviewEndRequest,
    InterviewEvaluationRequest,
    InterviewQuestionRequest,
    InterviewStartRequest,
)
from app.services.interview_service import interview_service

router = APIRouter(prefix="/interview", tags=["AI Interview Coach"])


@router.post("/questions")
def generate_interview_questions(
    request: InterviewQuestionRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        result = interview_service.generate_questions(request, current_user.id)
        return {"success": True, "message": "Interview questions generated successfully.", "data": result}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Interview question generation failed. Check the AI provider configuration.") from exc


@router.post("/evaluate")
def evaluate_answer(
    request: InterviewEvaluationRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        result = interview_service.evaluate_answer(request)
        return {"success": True, "message": "Interview answer evaluated successfully.", "data": result}
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Answer evaluation failed. Check the AI provider configuration.") from exc


@router.post("/start")
def start_interview(
    request: InterviewStartRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        result = interview_service.start_interview(request, current_user.id)
        return {"success": True, "message": "Interview started successfully.", "data": result}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to start interview. Check the AI provider configuration.") from exc


@router.post("/answer")
def submit_answer(
    request: InterviewAnswerRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        result = interview_service.submit_answer(request, current_user.id)
        return {"success": True, "message": "Answer evaluated successfully.", "data": result}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to evaluate answer. Check the AI provider configuration.") from exc


@router.post("/end")
def end_interview(
    request: InterviewEndRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        result = interview_service.end_interview(request, current_user.id)
        return {"success": True, "message": "Interview report generated successfully.", "data": result}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to generate the report. Check the AI provider configuration.") from exc
