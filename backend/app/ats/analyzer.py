import json
import re

from app.ai.llm import llm_service
from app.ai.prompts.ats_prompt import ATS_PROMPT


class ATSAnalyzer:

    @staticmethod
    def generate_feedback(
        resume_text: str,
        job_description: str,
        score_result: dict,
    ):

        prompt = ATS_PROMPT.format(
            resume=resume_text,
            job_description=job_description,
            ats_score=score_result["ats_score"],
            matching_skills=", ".join(score_result["matching_skills"]),
            missing_skills=", ".join(score_result["missing_skills"]),
        )

        response = llm_service.generate(prompt)

        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        if response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:

            return {
                "overall_feedback": response,
                "strengths": [],
                "weaknesses": [],
                "resume_summary": "",
                "improved_summary": "",
                "recommended_keywords": [],
                "improvement_suggestions": []
            }


ats_analyzer = ATSAnalyzer()