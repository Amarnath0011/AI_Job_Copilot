from fastapi import APIRouter, HTTPException

from app.models.ats_models import ATSRequest
from app.rag.retriever import get_retriever
from app.services.ats_service import ats_service

router = APIRouter(
    prefix="/ats",
    tags=["ATS"]
)


@router.post("/analyze")
def analyze_resume(request: ATSRequest):

    try:

        retriever = get_retriever(
            document_type="resume",
        )

        docs = retriever.invoke(request.job_description)

        if not docs:
            raise HTTPException(
                status_code=404,
                detail="No resume found for this session."
            )

        resume_text = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        result = ats_service.analyze(
            resume_text=resume_text,
            job_description=request.job_description,
        )

        return {
            "success": True,
            "message": "ATS analysis completed successfully.",
            "data": result,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )