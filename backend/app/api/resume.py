from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.services.resume_service import save_resume

router = APIRouter(prefix="/resume", tags=["Resume"])

MAX_RESUME_BYTES = 10 * 1024 * 1024
ALLOWED_TYPES = {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: Annotated[UploadFile, File(...)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    filename = (file.filename or "").lower()
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed.")
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="The uploaded file must be a PDF or DOCX.")
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(contents) > MAX_RESUME_BYTES:
        raise HTTPException(status_code=413, detail="Resume must be 10 MB or smaller.")

    result = save_resume(
        contents=contents,
        filename=file.filename or "resume.pdf",
        content_type=file.content_type or "application/pdf",
        user=current_user,
        db=db,
    )
    return {"success": True, "message": "Resume uploaded successfully.", "data": result}
