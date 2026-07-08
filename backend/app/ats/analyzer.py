from app.ai.llm import llm_service
from app.ai.prompts.ats_prompt import ATS_PROMPT

import json


class ATSAnalyzer:

    @staticmethod
    def analyze(
        resume_text,
        job_description,
        score_result,
    ):

        prompt = ATS_PROMPT.format(

            resume=resume_text,

            job_description=job_description,

            ats_score=score_result["ats_score"],

            matching_skills=", ".join(
                score_result["matching_skills"]
            ),

            missing_skills=", ".join(
                score_result["missing_skills"]
            )

        )

        response = llm_service.generate(prompt)

        try:
            return json.loads(response)

        except Exception:

            return {
                "overall_feedback": response
            }


ats_analyzer = ATSAnalyzer()