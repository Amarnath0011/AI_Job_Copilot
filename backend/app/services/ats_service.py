from app.ats.scorer import ATSScorer
from app.ats.analyzer import ats_analyzer


class ATSService:

    def analyze(
        self,
        resume_text: str,
        job_description: str,
    ):

        score = ATSScorer.score(
            resume_text=resume_text,
            job_description=job_description,
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