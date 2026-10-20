from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import Resume, User
from app.services.resume_service import MAX_RESUME_BYTES, save_resume

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: Annotated[UploadFile, File(...)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if not file.filename or not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Please upload a PDF resume.")
    contents = await file.read(MAX_RESUME_BYTES + 1)
    if len(contents) > MAX_RESUME_BYTES:
        raise HTTPException(status_code=413, detail="Resume must be 10 MB or smaller.")
    result = save_resume(contents, file.filename, file.content_type, current_user, db)
    return {"success": True, "message": "Resume uploaded successfully.", "data": result}


@router.get("/mine")
def list_my_resumes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )
    return {
        "success": True,
        "data": [
            {
                "resume_id": resume.id,
                "filename": resume.original_filename,
                "session_id": resume.session_id,
                "created_at": resume.created_at.isoformat() if resume.created_at else None,
            }
            for resume in resumes
        ],
    }
