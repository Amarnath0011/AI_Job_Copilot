from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_service import save_resume

router = APIRouter(prefix="/resume", tags=["Resume"])


ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    result = save_resume(file)

    return {
        "success": True,
        **result
    }