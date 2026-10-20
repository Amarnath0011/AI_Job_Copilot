from app.ai.prompts.interview import (
    INTERVIEW_EVALUATION_PROMPT,
    INTERVIEW_NEXT_QUESTION_PROMPT,
    INTERVIEW_QUESTION_PROMPT,
    INTERVIEW_REPORT_PROMPT,
    interview_evaluation_parser,
    interview_question_parser,
    interview_report_parser,
    next_question_parser,
)
from app.ai.prompts.interview_report import INTERVIEW_REPORT_PROMPT, interview_report_parser
from app.models.interview_models import (
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    InterviewEndRequest,
    InterviewEvaluationRequest,
    InterviewEvaluationResponse,
    InterviewHistoryItem,
    InterviewQuestionRequest,
    InterviewQuestionResponse,
    InterviewReportResponse,
    InterviewStartRequest,
    InterviewStartResponse,
)
from app.rag.retriever import get_retriever
from app.db.database import SessionLocal
from app.db.models import Resume
from app.services.llm_service import llm_service
from app.utils.parsers import LLMParser
from app.utils.session import session_manager


class InterviewService:
    """
    Service responsible for all interview-related AI features.
    """

    # ==========================================================
    # Private Helpers
    # ==========================================================

    def _get_resume_context(
        self,
        job_description: str,
        user_id: int,
        session_id: str,
    ) -> str:
        """
        Retrieve the most relevant resume chunks using RAG.
        """

        retriever = get_retriever(
            document_type="resume",
            session_id=session_id,
            user_id=user_id,
            k=5,
        )

        documents = retriever.invoke(job_description)

        if not documents:
            raise ValueError(
                "Resume not found. Please upload a resume first."
            )

        return "\n\n".join(
            doc.page_content
            for doc in documents
        )
        
        
    # ==========================================================
# Private Helpers
# ==========================================================

    def _build_interview_history(
        self,
        history: list[InterviewHistoryItem],
    ) -> str:
        """
        Build a compact interview summary for report generation.

        Instead of sending complete candidate answers,
        send only the evaluation summary for each question.
        """

        if not history:
            return "No interview history available."

        interview_summary = []

        for index, item in enumerate(history, start=1):

            evaluation = item.evaluation

            strengths = (
                ", ".join(evaluation.strengths)
                if evaluation.strengths
                else "None"
            )

            improvements = (
                ", ".join(evaluation.improvements)
                if evaluation.improvements
                else "None"
            )

            interview_summary.append(
                f"""
    Question {index}

    Question:
    {item.question}

    Overall Score:
    {evaluation.overall_score}/100

    Technical Score:
    {evaluation.technical_score}/100

    Communication Score:
    {evaluation.communication_score}/100

    Strengths:
    {strengths}

    Areas for Improvement:
    {improvements}

    Feedback:
    {evaluation.feedback}
    """.strip()
            )

        return "\n\n".join(interview_summary)


    # ==========================================================
    # Feature 5.1
    # ==========================================================

    def generate_questions(
        self,
        request: InterviewQuestionRequest,
        user_id: int,
    ) -> InterviewQuestionResponse:

        with SessionLocal() as db:
            resume = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).first()
            if resume is None:
                raise ValueError("Upload a resume before generating interview questions.")
            resume_session_id = resume.session_id
        resume_context = self._get_resume_context(
            request.job_description, user_id, resume_session_id
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

    # ==========================================================
    # Feature 5.2
    # ==========================================================

    def evaluate_answer(
        self,
        request: InterviewEvaluationRequest,
    ) -> InterviewEvaluationResponse:

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

    # ==========================================================
    # Internal
    # ==========================================================

    def generate_next_question(
        self,
        resume_context: str,
        job_description: str,
        history: list[InterviewHistoryItem],
        average_score: int,
    ) -> str:
        """
        Generate the next adaptive interview question.
        """

        history_text = "\n\n".join(
            [
                f"""
Question:
{item.question}

Answer:
{item.answer}

Score:
{item.evaluation.overall_score}

Feedback:
{item.evaluation.feedback}
"""
                for item in history
            ]
        )

        if not history_text:
            history_text = "No previous questions."

        messages = INTERVIEW_NEXT_QUESTION_PROMPT.format_messages(
            resume_context=resume_context,
            job_description=job_description,
            history=history_text,
            average_score=average_score,
        )

        response = llm_service.generate(messages)

        return next_question_parser.parse(response)

    # ==========================================================
    # Feature 5.3
    # ==========================================================

    def start_interview(
        self,
        request: InterviewStartRequest,
        user_id: int,
    ) -> InterviewStartResponse:
        """
        Start a new interview session.
        """

        with SessionLocal() as db:
            resume = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).first()
            if resume is None:
                raise ValueError("Upload a resume before starting an interview.")
            resume_id = resume.id
            resume_session_id = resume.session_id
        resume_context = self._get_resume_context(
            request.job_description, user_id, resume_session_id
        )

        first_question = self.generate_next_question(
            resume_context=resume_context,
            job_description=request.job_description,
            history=[],
            average_score=0,
        )

        session = session_manager.create_session(
            resume_context=resume_context,
            job_description=request.job_description,
            first_question=first_question,
            total_questions=5,
            user_id=user_id,
            resume_id=resume_id,
        )

        return InterviewStartResponse(
            session_id=session["session_id"],
            question_number=1,
            total_questions=5,
            question=first_question,
        )

    def submit_answer(
        self,
        request: InterviewAnswerRequest,
        user_id: int,
    ) -> InterviewAnswerResponse:
        """
        Evaluate answer and generate next adaptive question.
        """

        session = session_manager.get_session(
            request.session_id, user_id
        )

        if not session:
            raise ValueError(
                "Interview session not found."
            )

        evaluation = self.evaluate_answer(
            InterviewEvaluationRequest(
                question=session["current_question"],
                answer=request.answer,
            )
        )

        session_manager.add_history(
            session_id=request.session_id,
            answer=request.answer,
            evaluation=evaluation,
            user_id=user_id,
        )

        completed = session_manager.is_completed(
            request.session_id, user_id
        )

        if completed:

            return InterviewAnswerResponse(
                evaluation=evaluation,
                question_number=session["current_question_number"],
                total_questions=session["total_questions"],
                interview_completed=True,
                next_question=None,
            )

        next_question = self.generate_next_question(
            resume_context=session["resume_context"],
            job_description=session["job_description"],
            history=session_manager.get_history(
                request.session_id, user_id
            ),
            average_score=session_manager.get_average_score(
                request.session_id, user_id
            ),
        )

        session_manager.set_next_question(
            request.session_id,
            next_question,
            user_id,
        )

        updated_session = session_manager.get_session(
            request.session_id, user_id
        )

        return InterviewAnswerResponse(
            evaluation=evaluation,
            question_number=updated_session["current_question_number"],
            total_questions=updated_session["total_questions"],
            interview_completed=False,
            next_question=next_question,
        )

    def end_interview(
        self,
        request: InterviewEndRequest,
        user_id: int,
    ) -> InterviewReportResponse:
        """
        Generate the final interview report for a completed interview session.
        """

        session = session_manager.get_session(
            request.session_id, user_id
        )

        if not session:
            raise ValueError(
            "Interview session not found."
            )

        interview_history = self._build_interview_history(
            session["history"]
                   )

        messages = INTERVIEW_REPORT_PROMPT.format_messages(
            resume_context=session["resume_context"],
            job_description=session["job_description"],
            interview_history=interview_history,
            format_instructions=interview_report_parser.get_format_instructions(),
        )

        llm_response = llm_service.generate(messages)

        report = LLMParser.parse(
            llm_response,
            interview_report_parser,
        )

        # session_manager.delete_session(
        #     request.session_id
        # )

        return report


# ==========================================================
# Singleton Instance
# ==========================================================

interview_service = InterviewService()