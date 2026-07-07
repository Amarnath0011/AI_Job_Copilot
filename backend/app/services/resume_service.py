from pathlib import Path
import shutil
from fastapi import UploadFile

from app.services.parser import extract_text_from_pdf
from app.services.document_service import store_document

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_resume(file: UploadFile):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = ""

    if file.content_type == "application/pdf":
        extracted_text = extract_text_from_pdf(file_path)

        # Store in Chroma
        store_document(
            text=extracted_text,
            source=file.filename,
            document_type="resume"
        )

    return {
        "filename": file.filename,
        "size": file_path.stat().st_size,
        "path": str(file_path),
        "text": extracted_text
    }