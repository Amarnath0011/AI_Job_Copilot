from app.ats.scorer import ATSScorer
from app.ats.analyzer import ats_analyzer


class ATSService:
    """
    Orchestrates the complete ATS analysis workflow.
    """

    def analyze(
        self,
        resume_text: str,
        job_description: str,
    ):

        # Step 1: Calculate ATS score
        score = ATSScorer.score(
            resume_text=resume_text,
            job_description=job_description,
        )

        # Step 2: Generate AI feedback
        feedback = ats_analyzer.generate_feedback(
            resume_text=resume_text,
            job_description=job_description,
            ats_score=score["ats_score"],
            matching_skills=score["matching_skills"],
            missing_skills=score["missing_skills"],
        )

        # Step 3: Merge both results
        return {
            **score,
            "ai_feedback": feedback,
        }


ats_service = ATSService()