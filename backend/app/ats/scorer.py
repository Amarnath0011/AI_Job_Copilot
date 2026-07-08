from app.services.similarity_service import SimilarityService
from app.services.keyword_service import KeywordService


class ATSScorer:

    @staticmethod
    def score(
        resume_text: str,
        job_description: str,
    ):

        similarity = SimilarityService.calculate_similarity(
            resume_text,
            job_description,
        )

        resume_skills = KeywordService.extract(resume_text)
        jd_skills = KeywordService.extract(job_description)

        matching = sorted(resume_skills & jd_skills)
        missing = sorted(jd_skills - resume_skills)

        if jd_skills:
            keyword_score = (
                len(matching) / len(jd_skills)
            ) * 100
        else:
            keyword_score = 100

        # Weighted score
        semantic_score = similarity * 100
        ats_score = round(
            (semantic_score * 0.7) +
            (keyword_score * 0.30)
        )

        return {
            "ats_score": ats_score,
            "semantic_similarity": similarity,
            "matching_skills": matching,
            "missing_skills": missing,
        }