from app.services.keyword_service import KeywordService
from app.services.similarity_service import SimilarityService


class ATSScorer:
    """Deterministic ATS-style coverage score with an explainable breakdown."""

    @staticmethod
    def score(resume_text: str, job_description: str) -> dict:
        resume_skills = KeywordService.extract(resume_text)
        jd_skills = KeywordService.extract(job_description)

        matching = sorted(resume_skills & jd_skills)
        missing = sorted(jd_skills - resume_skills)

        keyword_score = (
            round((len(matching) / len(jd_skills)) * 100, 2)
            if jd_skills
            else None
        )

        similarity = SimilarityService.calculate_similarity(
            resume_text=resume_text,
            job_description=job_description,
        )
        semantic_score = round(similarity * 100, 2)

        # If the JD contains recognized skills, prioritize explicit requirements.
        # If it contains none, avoid falsely claiming 100% keyword coverage.
        if keyword_score is None:
            ats_score = round(semantic_score)
        else:
            ats_score = round((keyword_score * 0.60) + (semantic_score * 0.40))

        return {
            "ats_score": max(0, min(100, ats_score)),
            "keyword_score": keyword_score,
            "semantic_score": semantic_score,
            "semantic_similarity": similarity,
            "recognized_jd_skills": sorted(jd_skills),
            "matching_skills": matching,
            "missing_skills": missing,
        }
