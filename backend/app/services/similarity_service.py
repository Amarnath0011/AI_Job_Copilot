from math import sqrt


class SimilarityService:
    """Compare full documents in overlapping chunks to avoid embedding truncation."""

    CHUNK_SIZE = 900
    CHUNK_OVERLAP = 120

    @classmethod
    def _split_text(cls, text: str) -> list[str]:
        text = (text or "").strip()
        if not text:
            return []

        chunks: list[str] = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + cls.CHUNK_SIZE, text_length)
            if end < text_length:
                # Prefer ending at a paragraph or sentence boundary when nearby.
                boundary = max(
                    text.rfind("\n\n", start, end),
                    text.rfind("\n", start, end),
                    text.rfind(". ", start, end),
                )
                if boundary > start + (cls.CHUNK_SIZE // 2):
                    end = boundary + (2 if text[boundary:boundary + 2] == ". " else 0)

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end >= text_length:
                break
            start = max(end - cls.CHUNK_OVERLAP, start + 1)

        return chunks

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
        resume_chunks = cls._split_text(resume_text)
        jd_chunks = cls._split_text(job_description)
        if not resume_chunks or not jd_chunks:
            return 0.0

        # Import lazily so keyword/scorer tests don't load model weights.
        from app.ai.embeddings import embedding_model

        resume_vectors = embedding_model.embed_documents(resume_chunks)
        jd_vectors = embedding_model.embed_documents(jd_chunks)

        # For each JD chunk, use its best matching resume chunk. This measures
        # coverage across the JD while tolerating different section ordering.
        best_matches = [
            max(cls._cosine(resume_vector, jd_vector) for resume_vector in resume_vectors)
            for jd_vector in jd_vectors
        ]
        similarity = sum(best_matches) / len(best_matches)
        return round(max(0.0, min(1.0, float(similarity))), 4)
