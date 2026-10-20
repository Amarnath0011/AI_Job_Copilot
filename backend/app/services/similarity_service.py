from math import sqrt

from langchain_text_splitters import RecursiveCharacterTextSplitter


class SimilarityService:
    """Compare full documents in chunks to avoid embedding-model truncation."""

    _splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    @staticmethod
    def _cosine(left: list[float], right: list[float]) -> float:
        dot = sum(a * b for a, b in zip(left, right))
        left_norm = sqrt(sum(a * a for a in left))
        right_norm = sqrt(sum(b * b for b in right))
        if not left_norm or not right_norm:
            return 0.0
        return dot / (left_norm * right_norm)

    @classmethod
    def calculate_similarity(
        cls,
        resume_text: str,
        job_description: str,
    ) -> float:
        resume_chunks = cls._splitter.split_text(resume_text or "")
        jd_chunks = cls._splitter.split_text(job_description or "")
        if not resume_chunks or not jd_chunks:
            return 0.0

        # Import lazily so deterministic keyword/scorer tests don't load model weights.
        from app.ai.embeddings import embedding_model

        resume_vectors = embedding_model.embed_documents(resume_chunks)
        jd_vectors = embedding_model.embed_documents(jd_chunks)

        # For each JD chunk, use its best matching resume chunk. This scores coverage
        # across the entire JD while tolerating different section ordering and wording.
        best_matches = []
        for jd_vector in jd_vectors:
            best_matches.append(
                max(cls._cosine(resume_vector, jd_vector) for resume_vector in resume_vectors)
            )

        # Keep the original cosine scale (0..1 for this sentence embedding model);
        # do not rescale weak similarity into an artificially high score.
        similarity = sum(best_matches) / len(best_matches)
        return round(max(0.0, min(1.0, float(similarity))), 4)
