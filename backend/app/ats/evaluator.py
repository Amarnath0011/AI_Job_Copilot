import json
import logging
import re
from typing import Any

from app.models.ats_models import JDRequirement, RequirementEvidence
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

ACADEMIC_OR_JUNIOR_TERMS = [
    "college", "university", "academic", "coursework", "student",
    "bachelor", "master", "intern", "internship", "hobby", "school"
]


class EvidenceEvaluator:
    """
    Evaluates supporting resume evidence against JD requirements.
    Distinguishes exact verified matches, partial matches (e.g. academic vs professional experience),
    and unverified inferences.
    """

    @classmethod
    def evaluate_requirement_deterministic(
        cls,
        requirement: JDRequirement,
        evidence: RequirementEvidence,
    ) -> RequirementEvidence:
        """
        Applies deterministic rules to evaluate evidence for a requirement.
        """
        # Case 1: No evidence at all
        if not evidence.has_keyword_match and not evidence.has_semantic_match and not evidence.retrieved_passages:
            evidence.status = "no_evidence_found"
            evidence.score = 0.0
            evidence.confidence = 1.0
            evidence.reasoning = (
                f"No lexical or semantic evidence found in the evaluated resume for '{requirement.text}'. "
                "This indicates absence of evidence in the resume, not proof of candidate incapability."
            )
            return evidence

        all_evidence_text = " ".join(evidence.retrieved_passages).lower()

        # Case 2: Professional experience years mismatch check
        if requirement.years_required is not None and requirement.years_required > 0:
            # Check if evidence mentions the required skill/topic
            has_topic = evidence.has_keyword_match or (
                requirement.normalized_name and requirement.normalized_name.lower() in all_evidence_text
            )
            if not has_topic:
                evidence.status = "no_evidence_found"
                evidence.score = 0.0
                evidence.confidence = 0.95
                evidence.reasoning = f"No evidence found in resume regarding '{requirement.text}'."
                return evidence

            # Check if the evidence shows student / academic / hobby projects rather than verified professional years
            is_academic_only = any(term in all_evidence_text for term in ACADEMIC_OR_JUNIOR_TERMS)
            # Check if professional experience duration pattern is matched in resume
            years_pattern = re.compile(
                r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s*of)?\s*(?:hands-on\s+|professional\s+|work\s+)?experience",
                re.IGNORECASE,
            )
            resume_years_match = years_pattern.search(all_evidence_text)
            verified_years = float(resume_years_match.group(1)) if resume_years_match else None

            if verified_years is not None and verified_years >= requirement.years_required:
                evidence.status = "matched"
                evidence.score = 1.0
                evidence.confidence = 0.9
                evidence.reasoning = (
                    f"Evidence demonstrates {verified_years} years of experience, satisfying the requirement of "
                    f"{requirement.years_required}+ years for '{requirement.text}'."
                )
                return evidence
            elif is_academic_only or verified_years is None or verified_years < requirement.years_required:
                evidence.status = "partial_match"
                evidence.score = 0.5
                evidence.confidence = 0.85
                evidence.reasoning = (
                    f"Relevant knowledge/experience in '{requirement.normalized_name or requirement.text}' was found, "
                    f"but evidence reflects academic, project, or unverified duration rather than "
                    f"{requirement.years_required}+ years of verified professional experience."
                )
                return evidence

        # Case 3: Pure technical skill / tool / database / framework match
        if evidence.has_keyword_match:
            evidence.status = "matched"
            evidence.score = 1.0
            evidence.confidence = 0.95
            evidence.reasoning = (
                f"Direct supporting evidence for '{requirement.text}' was verified in the resume "
                f"(matching keywords: {', '.join(evidence.matching_keywords)})."
            )
            return evidence

        # Case 4: Semantic match without direct keyword match (synonym or contextual phrasing)
        if evidence.has_semantic_match and evidence.retrieved_passages:
            # Check for known contextual equivalents (e.g. REST API vs HTTP endpoints / FastAPI endpoints)
            req_lower = requirement.text.lower()
            if "rest" in req_lower and ("endpoint" in all_evidence_text or "fastapi" in all_evidence_text or "http" in all_evidence_text):
                evidence.status = "matched"
                evidence.score = 1.0
                evidence.confidence = 0.85
                evidence.reasoning = (
                    f"Semantic match: Resume demonstrates practical API endpoint implementation supporting '{requirement.text}'."
                )
                return evidence

            # General semantic candidate needing further contextual evaluation or partial credit
            evidence.status = "partial_match"
            evidence.score = 0.5
            evidence.confidence = 0.70
            evidence.reasoning = (
                f"Contextual semantic evidence found in resume passage, but exact keyword '{requirement.text}' "
                "was not explicitly verified."
            )
            return evidence

        # Fallback
        evidence.status = "uncertain"
        evidence.score = 0.0
        evidence.confidence = 0.5
        evidence.reasoning = "Evidence was ambiguous and could not be deterministically confirmed."
        return evidence

    @classmethod
    def batch_evaluate_with_llm(
        cls,
        items: list[tuple[JDRequirement, RequirementEvidence]],
    ) -> list[RequirementEvidence]:
        """
        Evaluates a batch of contextual or ambiguous requirements using LLMService.
        Only sends requirement and relevant snippet — never entire resume.
        """
        if not items:
            return []

        payload = []
        for req, ev in items:
            snippets = " | ".join(ev.retrieved_passages[:2])
            payload.append({
                "requirement_id": req.requirement_id,
                "requirement": req.text,
                "years_required": req.years_required,
                "evidence_snippet": snippets[:400],
            })

        prompt = f"""
You are an expert technical evaluator. Evaluate whether the provided evidence from a candidate's resume supports each job requirement.
Rules:
1. "matched": Evidence clearly and directly demonstrates the required skill/qualification.
2. "partial_match": Evidence shows related knowledge, academic coursework, or student projects, but lacks requested duration/depth.
3. "no_evidence_found": Evidence snippet is irrelevant or does not support the requirement.
4. "uncertain": Evidence is ambiguous.

Return a JSON array of objects with keys:
- "requirement_id": string
- "status": "matched" | "partial_match" | "no_evidence_found" | "uncertain"
- "score": 1.0 for matched, 0.5 for partial_match, 0.0 for others
- "reasoning": short 1-sentence explanation

Items to evaluate:
{json.dumps(payload, indent=2)}

JSON:
"""
        try:
            raw = llm_service.generate(prompt).strip()
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.startswith("```"):
                raw = raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

            parsed = json.loads(raw)
            result_map = {item["requirement_id"]: item for item in parsed if isinstance(item, dict) and "requirement_id" in item}

            evaluated: list[RequirementEvidence] = []
            for req, ev in items:
                llm_eval = result_map.get(req.requirement_id)
                if llm_eval:
                    status = llm_eval.get("status", ev.status)
                    if status in ("matched", "partial_match", "no_evidence_found", "uncertain"):
                        ev.status = status
                    ev.score = 1.0 if ev.status == "matched" else (0.5 if ev.status == "partial_match" else 0.0)
                    ev.reasoning = str(llm_eval.get("reasoning") or ev.reasoning)
                    ev.confidence = 0.85
                evaluated.append(ev)
            return evaluated
        except Exception as exc:
            logger.warning("LLM batch evaluation failed, preserving deterministic evaluation: %s", exc)
            return [ev for _, ev in items]

    @classmethod
    def evaluate_all(
        cls,
        requirements: list[JDRequirement],
        evidences: list[RequirementEvidence],
        use_llm: bool = False,
    ) -> list[RequirementEvidence]:
        """
        Evaluates all requirements against their collected evidences.
        """
        results: list[RequirementEvidence] = []
        needs_llm: list[tuple[JDRequirement, RequirementEvidence]] = []

        req_map = {r.requirement_id: r for r in requirements}

        for ev in evidences:
            req = req_map.get(ev.requirement_id)
            if not req:
                results.append(ev)
                continue

            # Deterministic evaluation first
            evaluated_ev = cls.evaluate_requirement_deterministic(req, ev)

            # If ambiguous and LLM requested, queue for batch LLM evaluation
            if use_llm and evaluated_ev.status in ("uncertain", "partial_match") and evaluated_ev.retrieved_passages:
                needs_llm.append((req, evaluated_ev))
            else:
                results.append(evaluated_ev)

        if needs_llm:
            llm_results = cls.batch_evaluate_with_llm(needs_llm)
            results.extend(llm_results)

        return results


evidence_evaluator = EvidenceEvaluator()
