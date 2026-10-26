import logging
from typing import Any

from app.ats.analyzer import ats_analyzer
from app.ats.scorer import ATSScorer
from app.rag.vector_store import vector_store as default_vector_store

logger = logging.getLogger(__name__)


class ATSService:
    """
    Coordinates requirement extraction, session-isolated evidence retrieval,
    evidence-based scoring, and grounded AI feedback generation.
    """

    def analyze(
        self,
        resume_text: str,
        job_description: str,
        session_id: str | None = None,
        vector_store: Any = None,
    ) -> dict[str, Any]:
        """
        Analyzes the complete extracted resume against the complete job description.
        """
        vs = vector_store if vector_store is not None else default_vector_store

        score = ATSScorer.score(
            resume_text=resume_text,
            job_description=job_description,
            session_id=session_id,
            vector_store=vs,
        )

        feedback = ats_analyzer.generate_feedback(
            resume_text=resume_text,
            job_description=job_description,
            score_result=score,
        )

        return {
            **score,
            "ai_feedback": feedback,
        }


ats_service = ATSService()