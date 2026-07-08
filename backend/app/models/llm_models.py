from pydantic import BaseModel

class ATSFeedback(BaseModel):
    overall_feedback: str

    strengths: list[str]

    weaknesses: list[str]

    resume_summary: str

    improved_summary: str

    recommended_keywords: list[str]

    improvement_suggestions: list[str]