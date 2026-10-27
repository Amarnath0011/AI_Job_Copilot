import os
from io import BytesIO
from typing import Any

import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, status


def _configure_cloudinary() -> None:
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
    if not all((cloud_name, api_key, api_secret)):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloudinary is not configured. Add its three credentials to backend/.env.",
        )
    cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret, secure=True)


def upload_resume_bytes(contents: bytes, public_id: str) -> dict[str, str]:
    _configure_cloudinary()
    try:
        result: dict[str, Any] = cloudinary.uploader.upload(
            BytesIO(contents),
            resource_type="raw",
            type="authenticated",
            folder="ai-job-copilot/resumes",
            public_id=f"{public_id}.pdf",
            overwrite=False,
            unique_filename=False,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Resume upload to Cloudinary failed. Check credentials and retry.") from exc
    secure_url, returned_public_id = result.get("secure_url"), result.get("public_id")
    if not secure_url or not returned_public_id:
        raise HTTPException(status_code=502, detail="Cloudinary returned incomplete upload metadata.")
    return {"secure_url": secure_url, "public_id": returned_public_id}


def delete_resume_asset(public_id: str) -> None:
    _configure_cloudinary()
    try:
        cloudinary.uploader.destroy(public_id, resource_type="raw", type="authenticated", invalidate=True)
    except Exception:
        # Remote cleanup failures must not undo a successful local database operation.
        pass
