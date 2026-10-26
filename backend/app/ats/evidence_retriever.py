import logging
import re
from typing import Any

from app.models.ats_models import JDRequirement, RequirementEvidence

logger = logging.getLogger(__name__)

# Common section headers in resumes
SECTION_PATTERNS = [
    (re.compile(r"(?:^|\n)\s*(?:technical\s+)?skills\b", re.IGNORECASE), "Skills"),
    (re.compile(r"(?:^|\n)\s*(?:work\s+)?experience\b", re.IGNORECASE), "Experience"),
    (re.compile(r"(?:^|\n)\s*projects?\b", re.IGNORECASE), "Projects"),
    (re.compile(r"(?:^|\n)\s*education\b", re.IGNORECASE), "Education"),
    (re.compile(r"(?:^|\n)\s*certifications?\b", re.IGNORECASE), "Certifications"),
    (re.compile(r"(?:^|\n)\s*summary\b", re.IGNORECASE), "Summary"),
]


class EvidenceRetriever:
    """
    Retrieves requirement-level supporting evidence across the complete resume
    and session-specific vector chunks.
    """

    @staticmethod
    def _find_section_for_match(text: str, match_pos: int) -> str | None:
        """
        Determines the resume section containing the match based on preceding headers.
        """
        preceding_text = text[:match_pos]
        last_found_section = None
        last_found_index = -1

        for pattern, section_name in SECTION_PATTERNS:
            for match in pattern.finditer(preceding_text):
                if match.start() > last_found_index:
                    last_found_index = match.start()
                    last_found_section = section_name

        return last_found_section

    @staticmethod
    def _extract_surrounding_passage(text: str, start: int, end: int, window: int = 150) -> str:
        """
        Extracts a clean sentence or passage around the match with boundary checking.
        """
        passage_start = max(0, start - window)
        passage_end = min(len(text), end + window)

        # Snap to newline or sentence boundary if possible
        if passage_start > 0:
            first_nl = text.find("\n", passage_start, start)
            if first_nl != -1:
                passage_start = first_nl + 1

        if passage_end < len(text):
            last_nl = text.rfind("\n", end, passage_end)
            if last_nl != -1 and last_nl > end:
                passage_end = last_nl

        snippet = text[passage_start:passage_end].strip()
        # Clean up whitespace
        return re.sub(r"\s+", " ", snippet)

    @classmethod
    def match_lexical_evidence(
        cls,
        requirement: JDRequirement,
        full_resume_text: str,
    ) -> tuple[list[str], list[str], str | None]:
        """
        Searches full_resume_text deterministically for requirement keywords or aliases.
        Returns:
            (matching_keywords, matching_passages, detected_section)
        """
        if not full_resume_text or not full_resume_text.strip():
            return [], [], None

        search_terms = []
        if requirement.normalized_name:
            search_terms.append(requirement.normalized_name)
        if requirement.text and requirement.text.lower() not in search_terms:
            search_terms.append(requirement.text.lower())
        for alias in requirement.aliases:
            if alias.lower() not in search_terms:
                search_terms.append(alias.lower())

        matching_keywords: list[str] = []
        passages: list[str] = []
        detected_sections: list[str] = []

        resume_lower = full_resume_text.lower()

        for term in search_terms:
            # Word boundary matching to avoid partial substring false positives
            pattern = r"\b" + re.escape(term) + r"\b"
            match = re.search(pattern, resume_lower)
            if match:
                matching_keywords.append(term)
                passage = cls._extract_surrounding_passage(
                    full_resume_text, match.start(), match.end()
                )
                if passage and passage not in passages:
                    passages.append(passage)
                section = cls._find_section_for_match(full_resume_text, match.start())
                if section and section not in detected_sections:
                    detected_sections.append(section)

        primary_section = detected_sections[0] if detected_sections else None
        return matching_keywords, passages, primary_section

    @classmethod
    def retrieve_semantic_evidence(
        cls,
        requirement: JDRequirement,
        session_id: str,
        vector_store: Any = None,
        k: int = 2,
    ) -> tuple[list[str], list[str], float | None]:
        """
        Performs session-isolated semantic retrieval against ChromaDB for a specific requirement.
        Returns:
            (retrieved_passages, source_chunk_ids, best_similarity_score)
        """
        if vector_store is None or not session_id:
            return [], [], None

        query = requirement.text
        if requirement.category and requirement.category != "other":
            query = f"{requirement.category.replace('_', ' ')}: {requirement.text}"

        where_filter = {
            "$and": [
                {"document_type": "resume"},
                {"session_id": session_id},
            ]
        }

        try:
            # First try similarity_search_with_relevance_scores or similarity_search_with_score
            docs_with_scores = []
            if hasattr(vector_store, "similarity_search_with_relevance_scores"):
                try:
                    docs_with_scores = vector_store.similarity_search_with_relevance_scores(
                        query, k=k, filter=where_filter
                    )
                except Exception:
                    # Fallback to similarity_search if relevance scores not supported
                    docs = vector_store.similarity_search(query, k=k, filter=where_filter)
                    docs_with_scores = [(doc, 0.75) for doc in docs]
            elif hasattr(vector_store, "similarity_search"):
                docs = vector_store.similarity_search(query, k=k, filter=where_filter)
                docs_with_scores = [(doc, 0.75) for doc in docs]

            passages: list[str] = []
            chunk_ids: list[str] = []
            best_score: float | None = None

            for item in docs_with_scores:
                if isinstance(item, tuple):
                    doc, score = item
                else:
                    doc = item
                    score = None

                content = doc.page_content.strip()
                if content and content not in passages:
                    passages.append(content)

                chunk_id = getattr(doc, "id", None) or doc.metadata.get("chunk_id") or doc.metadata.get("source", "chunk")
                if chunk_id and chunk_id not in chunk_ids:
                    chunk_ids.append(str(chunk_id))

                if score is not None:
                    # Normalize score to 0.0 - 1.0 range
                    norm_score = max(0.0, min(1.0, float(score)))
                    if best_score is None or norm_score > best_score:
                        best_score = norm_score

            return passages, chunk_ids, best_score

        except Exception as exc:
            logger.warning(
                "Semantic retrieval failed for requirement '%s' in session %s: %s",
                requirement.text,
                session_id,
                exc,
            )
            return [], [], None

    @classmethod
    def collect_evidence_for_requirement(
        cls,
        requirement: JDRequirement,
        full_resume_text: str,
        session_id: str,
        vector_store: Any = None,
        k: int = 2,
    ) -> RequirementEvidence:
        """
        Combines deterministic lexical evidence and session-isolated semantic evidence
        for a single JD requirement.
        """
        # 1. Deterministic search against full resume text
        kw_matches, kw_passages, detected_section = cls.match_lexical_evidence(
            requirement, full_resume_text
        )

        # 2. Semantic search against ChromaDB chunks for this session
        sem_passages, chunk_ids, sem_score = cls.retrieve_semantic_evidence(
            requirement, session_id, vector_store=vector_store, k=k
        )

        has_kw = len(kw_matches) > 0
        has_sem = len(sem_passages) > 0 and (sem_score is None or sem_score >= 0.55)

        # Deduplicate passages
        all_passages: list[str] = []
        for p in kw_passages + sem_passages:
            p_clean = re.sub(r"\s+", " ", p).strip()
            if p_clean and not any(p_clean in existing or existing in p_clean for existing in all_passages):
                all_passages.append(p_clean)

        return RequirementEvidence(
            requirement_id=requirement.requirement_id,
            requirement_text=requirement.text,
            category=requirement.category,
            importance=requirement.importance,
            required_or_preferred=requirement.required_or_preferred,
            weight=requirement.weight,
            matching_keywords=kw_matches,
            retrieved_passages=all_passages[:3],  # Keep top bounded passages
            source_chunk_ids=chunk_ids,
            similarity_score=sem_score,
            has_keyword_match=has_kw,
            has_semantic_match=has_sem,
            status="no_evidence_found",  # will be resolved by evaluator
            confidence=0.0,
            score=0.0,
            reasoning="",
        )


evidence_retriever = EvidenceRetriever()
