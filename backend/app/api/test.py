from fastapi import APIRouter

from app.ai.llm import llm_service

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)


@router.get("/llm")
def test_llm():

    prompt = """
Explain FastAPI in about 50 words.
"""

    response = llm_service.generate(prompt)

    return {
        "response": response
    }