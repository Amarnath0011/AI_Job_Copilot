from uuid import uuid4

from app.models.interview_models import (
    InterviewEvaluationResponse,
    InterviewHistoryItem,
)


class SessionManager:
    """
    Manages interview sessions.

    Current Storage:
        - In Memory Dictionary

    Future:
        - MongoDB
    """

    def __init__(self):
        self.sessions = {}

    # =====================================================
    # Session Lifecycle
    # =====================================================

    def create_session(
        self,
        resume_context: str,
        job_description: str,
        first_question: str,
        total_questions: int = 5,
    ) -> dict:
        """
        Create a new interview session.
        """

        session_id = str(uuid4())

        session = {
            "session_id": session_id,
            "resume_context": resume_context,
            "job_description": job_description,
            "current_question": first_question,
            "current_question_number": 1,
            "total_questions": total_questions,
            "average_score": 0,
            "history": [],
        }

        self.sessions[session_id] = session

        return session

    def get_session(
        self,
        session_id: str,
    ) -> dict | None:
        """
        Returns a session by ID.
        """

        return self.sessions.get(session_id)

    def delete_session(
        self,
        session_id: str,
    ) -> None:
        """
        Deletes an interview session.
        """

        self.sessions.pop(session_id, None)

    # =====================================================
    # Question Management
    # =====================================================

    def get_current_question(
        self,
        session_id: str,
    ) -> str:

        session = self.get_session(session_id)

        if not session:
            raise ValueError("Interview session not found.")

        return session["current_question"]

    def set_next_question(
        self,
        session_id: str,
        question: str,
    ) -> None:

        session = self.get_session(session_id)

        if not session:
            raise ValueError("Interview session not found.")

        session["current_question"] = question
        session["current_question_number"] += 1

    # =====================================================
    # History
    # =====================================================

    def add_history(
        self,
        session_id: str,
        answer: str,
        evaluation: InterviewEvaluationResponse,
    ) -> None:

        session = self.get_session(session_id)

        if not session:
            raise ValueError("Interview session not found.")

        history_item = InterviewHistoryItem(
            question=session["current_question"],
            answer=answer,
            evaluation=evaluation,
        )

        session["history"].append(history_item)

        self._update_average_score(session)

    # =====================================================
    # Helpers
    # =====================================================

    def is_completed(
        self,
        session_id: str,
    ) -> bool:

        session = self.get_session(session_id)

        if not session:
            raise ValueError("Interview session not found.")

        return (
            session["current_question_number"]
            >= session["total_questions"]
        )

    def get_history(
        self,
        session_id: str,
    ) -> list[InterviewHistoryItem]:

        session = self.get_session(session_id)

        if not session:
            raise ValueError("Interview session not found.")

        return session["history"]

    def get_average_score(
        self,
        session_id: str,
    ) -> int:

        session = self.get_session(session_id)

        if not session:
            raise ValueError("Interview session not found.")

        return session["average_score"]

    def _update_average_score(
        self,
        session: dict,
    ) -> None:
        """
        Recalculate average interview score.
        """

        history = session["history"]

        if not history:
            session["average_score"] = 0
            return

        total = sum(
            item.evaluation.overall_score
            for item in history
        )

        session["average_score"] = round(
            total / len(history)
        )


# =========================================================
# Singleton Instance
# =========================================================

session_manager = SessionManager()