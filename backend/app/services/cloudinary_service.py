import os
from io import BytesIO
from typing import Any

import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, status


def upload_resume_bytes(contents: bytes, public_id: str) -> dict[str, Any]:
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
    if not all((cloud_name, api_key, api_secret)):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloudinary is not configured. Set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in backend/.env.",
        )

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )
    try:
        result = cloudinary.uploader.upload(
            BytesIO(contents),
            resource_type="raw",
            folder="ai-job-copilot/resumes",
            public_id=public_id,
            overwrite=False,
            unique_filename=False,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Resume upload to Cloudinary failed. Check your Cloudinary configuration and try again.",
        ) from exc

    secure_url = result.get("secure_url")
    returned_public_id = result.get("public_id")
    if not secure_url or not returned_public_id:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Cloudinary did not return the expected file URL and public ID.",
        )
    return {"secure_url": secure_url, "public_id": returned_public_id}
