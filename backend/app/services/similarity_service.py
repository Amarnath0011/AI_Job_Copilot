import logging
import re
from typing import Any

from sklearn.metrics.pairwise import cosine_similarity

from app.ai.embeddings import embedding_model

logger = logging.getLogger(__name__)

# all-MiniLM-L6-v2 max sequence length is typically 256 tokens (~1000 chars)
SAFE_EMBEDDING_WINDOW = 900
CHUNK_STEP = 600


class SimilarityService:
    """
    Computes semantic similarity safely across short and long documents.
    Avoids silent truncation by using a chunked, top-relevant matching strategy.
    """

    CHUNK_SIZE = SAFE_EMBEDDING_WINDOW

    @classmethod
    def _split_text(cls, text: str, max_chars: int = SAFE_EMBEDDING_WINDOW, step: int = CHUNK_STEP) -> list[str]:
        return cls._chunk_text(text, max_chars=max_chars, step=step)

    @classmethod
    def _chunk_text(cls, text: str, max_chars: int = SAFE_EMBEDDING_WINDOW, step: int = CHUNK_STEP) -> list[str]:
        """
        Splits text into bounded sliding windows to stay within embedding model limits.
        """
        clean_text = text.strip()
        if len(clean_text) <= max_chars:
            return [clean_text] if clean_text else []

        chunks: list[str] = []
        start = 0
        while start < len(clean_text):
            end = min(len(clean_text), start + max_chars)
            # Find nearest newline or sentence break if possible
            if end < len(clean_text):
                break_point = clean_text.rfind("\n", start + step, end)
                if break_point != -1:
                    end = break_point + 1
            chunk = clean_text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += step

        return chunks

    @classmethod
    def calculate_similarity(
        cls,
        resume_text: str,
        job_description: str,
    ) -> float:
        """
        Calculates cosine similarity between resume and job description.
        For long resumes, aggregates the best matching chunk representations
        so that skills in later sections contribute rather than being silently truncated.
        """
        if not resume_text.strip() or not job_description.strip():
            return 0.0

        try:
            resume_chunks = cls._chunk_text(resume_text)
            jd_chunks = cls._chunk_text(job_description)

            if not resume_chunks or not jd_chunks:
                return 0.0

            # If both are compact, embed directly
            if len(resume_chunks) == 1 and len(jd_chunks) == 1:
                resume_emb = embedding_model.embed_query(resume_chunks[0])
                jd_emb = embedding_model.embed_query(jd_chunks[0])
                sim = cosine_similarity([resume_emb], [jd_emb])[0][0]
                return round(float(max(0.0, min(1.0, sim))), 2)

            # For multi-chunk documents:
            # Embed all resume chunks and JD chunks
            resume_embeddings = embedding_model.embed_documents(resume_chunks)
            jd_embeddings = embedding_model.embed_documents(jd_chunks)

            # Compute pairwise similarity matrix: [len(jd_chunks) x len(resume_chunks)]
            sim_matrix = cosine_similarity(jd_embeddings, resume_embeddings)

            # For each JD chunk, find the max similarity with any resume chunk
            max_sims_per_jd = sim_matrix.max(axis=1)

            # Document-level semantic score is the average of how well each JD chunk found a match
            avg_best_similarity = float(max_sims_per_jd.mean())
            return round(float(max(0.0, min(1.0, avg_best_similarity))), 2)

        except Exception as exc:
            logger.warning("Embedding similarity calculation encountered error, falling back to lexical overlap: %s", exc)
            return cls._fallback_lexical_similarity(resume_text, job_description)

    @staticmethod
    def _fallback_lexical_similarity(text1: str, text2: str) -> float:
        """
        Token-overlap fallback if embedding fails.
        """
        tokens1 = set(re.findall(r"\b[a-zA-Z0-9#\+\.]{2,}\b", text1.lower()))
        tokens2 = set(re.findall(r"\b[a-zA-Z0-9#\+\.]{2,}\b", text2.lower()))
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return round(float(intersection / union) if union > 0 else 0.0, 2)