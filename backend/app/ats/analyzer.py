import json
import logging
import re
from typing import Any

from app.ai.prompts.ats_prompt import ATS_PROMPT
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class ATSAnalyzer:
    """
    Generates grounded AI feedback based on structured requirement evaluation results.
    Does NOT recalculate or modify the deterministic ATS score.
    """

    @classmethod
    def generate_feedback(
        cls,
        resume_text: str,
        job_description: str,
        score_result: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generates structured feedback for the candidate grounded in verified evidence.
        """
        matching = score_result.get("matching_skills", [])
        missing = score_result.get("missing_skills", [])
        partial = score_result.get("partial_matches", [])
        uncertain = score_result.get("uncertain_requirements", [])
        score = score_result.get("ats_score", 0)

        # Truncate JD summary if very long to stay within token limits
        jd_summary = job_description[:1500]

        matching_str = ", ".join(matching) if matching else "No verified direct matches found."
        partial_str = ", ".join(partial) if partial else "No partial matches found."
        missing_str = ", ".join(missing) if missing else "No missing requirements detected."
        uncertain_str = ", ".join(uncertain) if uncertain else "None."
        summary_str = (
            f"Matched: {len(matching)}, Partial: {len(partial)}, "
            f"No Evidence Found: {len(missing)}, Uncertain: {len(uncertain)}"
        )

        prompt = ATS_PROMPT.format(
            job_description=jd_summary,
            ats_score=score,
            matching_skills=matching_str,
            partial_matches=partial_str,
            missing_skills=missing_str,
            uncertain_requirements=uncertain_str,
            evidence_summary=summary_str,
        )

        try:
            response = llm_service.generate(prompt).strip()

            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()

            feedback_data = json.loads(response)

            # Ensure all required keys exist
            return {
                "overall_feedback": str(feedback_data.get("overall_feedback", "ATS evaluation completed.")),
                "strengths": list(feedback_data.get("strengths", []))[:3],
                "weaknesses": list(feedback_data.get("weaknesses", []))[:3],
                "resume_summary": str(feedback_data.get("resume_summary", "")),
                "improved_summary": str(feedback_data.get("improved_summary", "")),
                "recommended_keywords": list(feedback_data.get("recommended_keywords", []))[:8],
                "improvement_suggestions": list(feedback_data.get("improvement_suggestions", []))[:3],
            }

        except Exception as exc:
            logger.warning("AI feedback generation encountered an error or invalid JSON: %s", exc)
            return cls._generate_deterministic_fallback(matching, missing, partial, score)

    @classmethod
    def _generate_deterministic_fallback(
        cls,
        matching: list[str],
        missing: list[str],
        partial: list[str],
        score: int,
    ) -> dict[str, Any]:
        """
        Guaranteed fallback feedback when LLM is unavailable or JSON fails.
        """
        strengths = [
            f"Demonstrated verified evidence for {skill}."
            for skill in matching[:3]
        ]
        if not strengths:
            strengths = ["Resume structure is legible and parsed successfully."]

        weaknesses = []
        if partial:
            weaknesses.append(f"Gaps in verified professional experience depth for: {', '.join(partial[:2])}.")
        if missing:
            weaknesses.append(f"No supporting evidence found for required skills: {', '.join(missing[:2])}.")
        if not weaknesses:
            weaknesses = ["No major missing technical requirements identified."]

        suggestions = []
        if missing:
            suggestions.append(f"Add explicit project details or experience covering {missing[0]}.")
        if partial:
            suggestions.append(f"Clarify professional timeline and duration for {partial[0]}.")
        suggestions.append("Align bullet points with measurable impact and target role keywords.")

        recommended = (missing[:5] + partial[:3])[:8]

        return {
            "overall_feedback": (
                f"Candidate achieved an ATS score of {score}/100. "
                f"Verified matches were found for {len(matching)} requirement(s), while {len(missing)} "
                "requirement(s) lacked supporting evidence in the evaluated resume."
            ),
            "strengths": strengths[:3],
            "weaknesses": weaknesses[:3],
            "resume_summary": "Extracted technical resume evaluated across job description requirements.",
            "improved_summary": "Technical profile demonstrating hands-on engineering experience and problem-solving.",
            "recommended_keywords": recommended,
            "improvement_suggestions": suggestions[:3],
        }


ats_analyzer = ATSAnalyzer()