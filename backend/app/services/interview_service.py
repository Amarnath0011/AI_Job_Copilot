import json
import re

from app.ai.prompts.interview import INTERVIEW_QUESTION_PROMPT
from app.models.interview_models import (
    InterviewQuestionRequest,
    InterviewQuestionResponse,
)
from app.rag.retriever import get_retriever
from app.services.llm_service import llm_service


class InterviewService:
    """
    Service responsible for generating personalized interview questions.
    """

    def __extract_json(self, text: str) -> dict:
        """
        Extracts JSON from LLM output.
        """

        text = text.strip()

        # Remove markdown fences
        text = re.sub(r"^```json", "", text)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)

        # Find JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            raise ValueError("No valid JSON found in LLM response.")

        return json.loads(match.group())

    def generate_questions(
        self,
        request: InterviewQuestionRequest,
    ) -> InterviewQuestionResponse:

        retriever = get_retriever(
            document_type="resume",
            k=5,
        )

        documents = retriever.invoke(request.job_description)

        if not documents:
            raise ValueError(
                "Resume not found. Please upload a resume first."
            )

        resume_context = "\n\n".join(
            doc.page_content
            for doc in documents
        )

        prompt = INTERVIEW_QUESTION_PROMPT.format(
            resume_context=resume_context,
            job_description=request.job_description,
        )

        llm_response = llm_service.generate(prompt)

        data = self.__extract_json(llm_response)

        return InterviewQuestionResponse(
            technical=data.get("technical", []),
            behavioral=data.get("behavioral", []),
            hr=data.get("hr", []),
        )


interview_service = InterviewService()