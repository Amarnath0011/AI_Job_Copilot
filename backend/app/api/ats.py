from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import Resume, User
from app.models.ats_models import ATSRequest
from app.rag.retriever import get_retriever
from app.services.ats_service import ats_service

router = APIRouter(prefix="/ats", tags=["ATS"])


@router.post("/analyze")
def analyze_resume(
    request: ATSRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resume = db.query(Resume).filter(
        Resume.session_id == request.session_id,
        Resume.user_id == current_user.id,
    ).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume session not found for this user.")

    retriever = get_retriever(
        document_type="resume",
        session_id=resume.session_id,
        user_id=current_user.id,
        k=5,
    )
    docs = retriever.invoke(request.job_description)
    resume_text = "\n\n".join(doc.page_content for doc in docs) or resume.extracted_text
    if not resume_text.strip():
        raise HTTPException(status_code=404, detail="No readable resume text is available.")

    try:
        result = ats_service.analyze(resume_text=resume_text, job_description=request.job_description)
    except Exception as exc:
        # Keep implementation details out of client responses.
        raise HTTPException(status_code=502, detail="ATS analysis failed. Check the AI provider configuration and retry.") from exc

    return {"success": True, "message": "ATS analysis completed successfully.", "data": result}
