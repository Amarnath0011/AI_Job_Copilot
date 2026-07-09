from app.ai.prompts.interview import (
    INTERVIEW_EVALUATION_PROMPT,
    INTERVIEW_QUESTION_PROMPT,
    interview_evaluation_parser,
    interview_question_parser,
)
from app.models.interview_models import (
    InterviewEvaluationRequest,
    InterviewEvaluationResponse,
    InterviewQuestionRequest,
    InterviewQuestionResponse,
)
from app.rag.retriever import get_retriever
from app.services.llm_service import llm_service
from app.utils.parsers import LLMParser


class InterviewService:
    """
    Service responsible for interview related AI features.
    """

    def generate_questions(
        self,
        request: InterviewQuestionRequest,
    ) -> InterviewQuestionResponse:
        """
        Generate personalized interview questions using:
        - Resume Context (RAG)
        - Job Description
        """

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

        messages = INTERVIEW_QUESTION_PROMPT.format_messages(
            resume_context=resume_context,
            job_description=request.job_description,
            format_instructions=interview_question_parser.get_format_instructions(),
        )

        llm_response = llm_service.generate(messages)

        return LLMParser.parse(
            llm_response,
            interview_question_parser,
        )

    def evaluate_answer(
        self,
        request: InterviewEvaluationRequest,
    ) -> InterviewEvaluationResponse:
        """
        Evaluate a candidate's interview answer.
        """

        messages = INTERVIEW_EVALUATION_PROMPT.format_messages(
            question=request.question,
            answer=request.answer,
            format_instructions=interview_evaluation_parser.get_format_instructions(),
        )

        llm_response = llm_service.generate(messages)

        return LLMParser.parse(
            llm_response,
            interview_evaluation_parser,
        )


# Singleton instance
interview_service = InterviewService()