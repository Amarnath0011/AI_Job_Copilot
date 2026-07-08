from fastapi import APIRouter

from app.ai.llm import llm_service
from app.ai.prompts.ats_prompt import ATS_PROMPT

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)


@router.get("/ats-prompt")
def test_ats_prompt():

    prompt = ATS_PROMPT.format(
        resume="""
Java Backend Developer
Spring Boot
MySQL
REST APIs
Git
""",
        job_description="""
Looking for a Java Backend Developer with
Spring Boot
Docker
AWS
MySQL
REST APIs
""",
        ats_score=75,
        matching_skills="Java, Spring Boot, MySQL, REST APIs",
        missing_skills="Docker, AWS",
    )

    response = llm_service.generate(prompt)

    return {
        "response": response
    }