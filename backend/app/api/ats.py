import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import Resume, User
from app.models.ats_models import ATSRequest
from app.services.ats_service import ats_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ats", tags=["ATS"])


@router.post("/analyze")
def analyze_resume(
    request: ATSRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Evaluates the candidate's complete resume against the job description using
    requirement-level evidence retrieval and scoring.
    """
    resume = db.query(Resume).filter(
        Resume.session_id == request.session_id,
        Resume.user_id == current_user.id,
    ).first()

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume session not found for this user."
        )

    full_resume_text = (resume.extracted_text or "").strip()
    if not full_resume_text:
        raise HTTPException(
            status_code=404,
            detail="No readable resume text is available."
        )

    try:
        result = ats_service.analyze(
            resume_text=full_resume_text,
            job_description=request.job_description,
            session_id=resume.session_id,
        )
    except Exception as exc:
        logger.error(
            "ATS analysis failed for user_id=%s, session_id=%s: %s",
            current_user.id,
            request.session_id,
            exc,
            exc_info=True,
        )
        raise HTTPException(
            status_code=502,
            detail="ATS analysis failed. Check the AI provider configuration and retry."
        ) from exc

    return {
        "success": True,
        "message": "ATS analysis completed successfully.",
        "data": result,
    }
