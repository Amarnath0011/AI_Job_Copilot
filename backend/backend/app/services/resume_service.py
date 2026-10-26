from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Resume, User
from app.rag.document_store import store_document
from app.services.cloudinary_service import upload_resume_bytes
from app.services.parser import extract_text_from_pdf

MAX_RESUME_BYTES = 10 * 1024 * 1024


def save_resume(contents: bytes, filename: str, content_type: str, user: User, db: Session) -> dict:
    if not contents:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(contents) > MAX_RESUME_BYTES:
        raise HTTPException(status_code=413, detail="Resume must be 10 MB or smaller.")

    extension = Path(filename).suffix.lower()
    if extension not in {".pdf", ".docx"}:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed.")
    if extension != ".pdf":
        raise HTTPException(status_code=415, detail="DOCX upload is accepted, but text extraction is not yet implemented. Please upload a PDF for AI analysis.")

    extracted_text = extract_text_from_pdf(BytesIO(contents))
    if not extracted_text.strip():
        raise HTTPException(status_code=422, detail="No readable text was found in this PDF.")

    session_id = str(uuid4())
    uploaded = upload_resume_bytes(contents, session_id)
    resume = Resume(
        id=str(uuid4()),
        session_id=session_id,
        user_id=user.id,
        original_filename=Path(filename).name[:255],
        cloudinary_url=uploaded["secure_url"],
        cloudinary_public_id=uploaded["public_id"],
        extracted_text=extracted_text,
    )
    try:
        db.add(resume)
        db.commit()
        db.refresh(resume)
    except Exception:
        db.rollback()
        raise

    try:
        store_document(
            text=extracted_text,
            source=resume.id,
            document_type="resume",
            session_id=session_id,
            user_id=str(user.id),
        )
    except Exception:
        # The uploaded resume remains safely stored and can be re-indexed later.
        # Do not silently lose the durable database record.
        raise HTTPException(status_code=500, detail="Resume was uploaded, but indexing failed. Please retry or contact support.")

    return {
        "resume_id": resume.id,
        "filename": resume.original_filename,
        "size": len(contents),
        "url": resume.cloudinary_url,
        "session_id": resume.session_id,
        "text": extracted_text,
    }
