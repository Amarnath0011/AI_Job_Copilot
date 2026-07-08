from sklearn.metrics.pairwise import cosine_similarity

from app.ai.embeddings import embedding_model


class SimilarityService:

    @staticmethod
    def calculate_similarity(
        resume_text: str,
        job_description: str,
    ) -> float:

        resume_embedding = embedding_model.embed_query(
            resume_text
        )

        jd_embedding = embedding_model.embed_query(
            job_description
        )

        similarity = cosine_similarity(
            [resume_embedding],
            [jd_embedding]
        )[0][0]

        return round(float(similarity), 2)