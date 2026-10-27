import logging
from typing import Any

from app.models.ats_models import RequirementEvidence
from app.services.keyword_service import KeywordService
from app.services.similarity_service import SimilarityService

logger = logging.getLogger(__name__)


class ATSScorer:
    """
    Computes an explainable, reproducible weighted ATS score grounded in requirement-level evidence.
    Does NOT rely on single full-document embedding or arbitrary top-k chunk limits.
    """

    @classmethod
    def compute_score(
        cls,
        evidence_list: list[RequirementEvidence],
        semantic_similarity: float = 0.0,
    ) -> dict[str, Any]:
        """
        Computes weighted ATS score, category breakdowns, and coverage metrics from requirement results.
        """
        if not evidence_list:
            return {
                "ats_score": 0,
                "weighted_coverage_score": 0.0,
                "keyword_score": 0.0,
                "semantic_score": round(float(semantic_similarity) * 100.0, 2),
                "evaluation_coverage": 0.0,
                "keyword_coverage": 0.0,
                "semantic_evidence_coverage": 0.0,
                "semantic_similarity": round(float(semantic_similarity), 2),
                "matching_skills": [],
                "missing_skills": [],
                "partial_matches": [],
                "uncertain_requirements": [],
                "evidence_summary": {
                    "matched": 0,
                    "partial_match": 0,
                    "no_evidence_found": 0,
                    "uncertain": 0,
                },
                "score_breakdown": {
                    "by_category": {},
                    "total_requirements": 0,
                    "total_evaluated_weight": 0.0,
                    "total_weight": 0.0,
                },
                "requirement_results": [],
                "analysis_status": "no_requirements_found",
            }

        valid_evidences = [ev for ev in evidence_list if ev.weight > 0]
        total_weight = sum(ev.weight for ev in valid_evidences)

        if total_weight <= 0:
            total_weight = float(len(valid_evidences)) if valid_evidences else 1.0

        total_points = sum(ev.weight * ev.score for ev in valid_evidences)
        weighted_coverage = (total_points / total_weight) * 100.0 if total_weight > 0 else 0.0
        final_ats_score = int(round(weighted_coverage))

        matching_skills: list[str] = []
        partial_matches: list[str] = []
        missing_skills: list[str] = []
        uncertain_requirements: list[str] = []

        keyword_match_count = 0
        semantic_match_count = 0
        evaluated_weight = 0.0

        by_category: dict[str, dict[str, Any]] = {}

        for ev in valid_evidences:
            cat = ev.category or "other"
            if cat not in by_category:
                by_category[cat] = {
                    "total": 0,
                    "matched": 0,
                    "partial": 0,
                    "missing": 0,
                    "uncertain": 0,
                    "total_weight": 0.0,
                    "earned_points": 0.0,
                }

            by_category[cat]["total"] += 1
            by_category[cat]["total_weight"] += ev.weight
            by_category[cat]["earned_points"] += ev.weight * ev.score

            if ev.has_keyword_match:
                keyword_match_count += 1
            if ev.has_semantic_match:
                semantic_match_count += 1

            if ev.status == "matched":
                matching_skills.append(ev.requirement_text)
                by_category[cat]["matched"] += 1
                evaluated_weight += ev.weight
            elif ev.status == "partial_match":
                partial_matches.append(ev.requirement_text)
                by_category[cat]["partial"] += 1
                evaluated_weight += ev.weight
            elif ev.status == "no_evidence_found":
                missing_skills.append(ev.requirement_text)
                by_category[cat]["missing"] += 1
                evaluated_weight += ev.weight
            else:
                uncertain_requirements.append(ev.requirement_text)
                by_category[cat]["uncertain"] += 1

        total_reqs = len(valid_evidences)
        evaluation_coverage = round((evaluated_weight / total_weight) * 100.0, 2) if total_weight > 0 else 0.0
        keyword_coverage = round((keyword_match_count / total_reqs) * 100.0, 2) if total_reqs > 0 else 0.0
        semantic_evidence_coverage = round((semantic_match_count / total_reqs) * 100.0, 2) if total_reqs > 0 else 0.0

        for cat, stats in by_category.items():
            cat_weight = stats["total_weight"]
            stats["coverage_pct"] = round((stats["earned_points"] / cat_weight) * 100.0, 2) if cat_weight > 0 else 0.0

        analysis_status = "completed" if not uncertain_requirements else "partial"

        return {
            "ats_score": final_ats_score,
            "weighted_coverage_score": round(weighted_coverage, 2),
            "keyword_score": keyword_coverage,
            "semantic_score": round(float(semantic_similarity) * 100.0, 2),
            "evaluation_coverage": evaluation_coverage,
            "keyword_coverage": keyword_coverage,
            "semantic_evidence_coverage": semantic_evidence_coverage,
            "semantic_similarity": round(float(semantic_similarity), 2),
            "matching_skills": sorted(matching_skills),
            "missing_skills": sorted(missing_skills),
            "partial_matches": sorted(partial_matches),
            "uncertain_requirements": sorted(uncertain_requirements),
            "evidence_summary": {
                "matched": len(matching_skills),
                "partial_match": len(partial_matches),
                "no_evidence_found": len(missing_skills),
                "uncertain": len(uncertain_requirements),
            },
            "score_breakdown": {
                "by_category": by_category,
                "total_requirements": total_reqs,
                "total_evaluated_weight": round(evaluated_weight, 2),
                "total_weight": round(total_weight, 2),
            },
            "requirement_results": [ev.model_dump() for ev in valid_evidences],
            "analysis_status": analysis_status,
        }

    @classmethod
    def score(
        cls,
        resume_text: str,
        job_description: str,
        session_id: str | None = None,
        vector_store: Any = None,
    ) -> dict[str, Any]:
        """
        Legacy-compatible entry point. Computes requirement-level evaluation
        over the entire resume text and session chunks.
        """
        from app.ats.evidence_retriever import evidence_retriever
        from app.ats.evaluator import evidence_evaluator
        from app.ats.requirement_extractor import requirement_extractor

        # 1. Extract requirements from JD
        requirements = requirement_extractor.extract_requirements(job_description)

        # 2. Supplementary bounded semantic similarity
        similarity = SimilarityService.calculate_similarity(resume_text, job_description)

        if not requirements:
            return cls.compute_score([], semantic_similarity=similarity)

        # 3. Retrieve evidence across full resume & session chunks
        evidences = [
            evidence_retriever.collect_evidence_for_requirement(
                requirement=req,
                full_resume_text=resume_text,
                session_id=session_id or "",
                vector_store=vector_store,
            )
            for req in requirements
        ]

        # 4. Evaluate evidence
        evaluated_evidences = evidence_evaluator.evaluate_all(requirements, evidences)

        # 5. Compute structured score
        return cls.compute_score(evaluated_evidences, semantic_similarity=similarity)