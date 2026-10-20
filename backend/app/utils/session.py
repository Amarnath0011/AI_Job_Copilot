from uuid import uuid4

from app.db.database import SessionLocal
from app.db.models import InterviewSession, Resume
from app.models.interview_models import InterviewEvaluationResponse, InterviewHistoryItem


def generate_session_id() -> str:
    return str(uuid4())


def _evaluation_dict(evaluation: InterviewEvaluationResponse) -> dict:
    return evaluation.model_dump()


def _history_item(raw: dict) -> InterviewHistoryItem:
    return InterviewHistoryItem.model_validate(raw)


class SessionManager:
    """SQLAlchemy-backed interview session store; no process-local session state."""

    def create_session(
        self,
        resume_context: str,
        job_description: str,
        first_question: str,
        total_questions: int = 5,
        user_id: int | None = None,
        resume_id: str | None = None,
    ) -> dict:
        if user_id is None:
            raise ValueError("Authenticated user is required to create an interview session.")
        with SessionLocal() as db:
            resume = db.query(Resume).filter(
                Resume.user_id == user_id,
                Resume.id == resume_id if resume_id else True,
            ).order_by(Resume.created_at.desc()).first()
            if resume is None:
                raise ValueError("Upload a resume before starting an interview.")
            row = InterviewSession(
                id=str(uuid4()),
                user_id=user_id,
                resume_id=resume.id,
                resume_context=resume_context,
                job_description=job_description,
                current_question=first_question,
                current_question_number=1,
                total_questions=total_questions,
                average_score=0,
                history=[],
                is_completed=False,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return self._to_dict(row)

    def _to_dict(self, row: InterviewSession) -> dict:
        return {
            "session_id": row.id,
            "user_id": row.user_id,
            "resume_id": row.resume_id,
            "resume_context": row.resume_context,
            "job_description": row.job_description,
            "current_question": row.current_question,
            "current_question_number": row.current_question_number,
            "total_questions": row.total_questions,
            "average_score": row.average_score,
            "history": [_history_item(item) for item in (row.history or [])],
            "is_completed": row.is_completed,
        }

    def get_session(self, session_id: str, user_id: int | None = None) -> dict | None:
        if user_id is None:
            return None
        with SessionLocal() as db:
            row = db.query(InterviewSession).filter(
                InterviewSession.id == session_id,
                InterviewSession.user_id == user_id,
            ).first()
            return self._to_dict(row) if row else None

    def delete_session(self, session_id: str, user_id: int | None = None) -> None:
        if user_id is None:
            return
        with SessionLocal() as db:
            row = db.query(InterviewSession).filter(
                InterviewSession.id == session_id,
                InterviewSession.user_id == user_id,
            ).first()
            if row:
                db.delete(row)
                db.commit()

    def set_next_question(self, session_id: str, question: str, user_id: int | None = None) -> None:
        with SessionLocal() as db:
            row = self._owned_row(db, session_id, user_id)
            row.current_question = question
            row.current_question_number += 1
            db.commit()

    def add_history(self, session_id: str, answer: str, evaluation: InterviewEvaluationResponse, user_id: int | None = None) -> None:
        with SessionLocal() as db:
            row = self._owned_row(db, session_id, user_id)
            history = list(row.history or [])
            history.append({
                "question": row.current_question,
                "answer": answer,
                "evaluation": _evaluation_dict(evaluation),
            })
            row.history = history
            row.average_score = round(sum(item["evaluation"]["overall_score"] for item in history) / len(history))
            row.is_completed = len(history) >= row.total_questions
            db.commit()

    def _owned_row(self, db, session_id: str, user_id: int | None):
        if user_id is None:
            raise ValueError("Authenticated user is required.")
        row = db.query(InterviewSession).filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == user_id,
        ).first()
        if row is None:
            raise ValueError("Interview session not found.")
        return row

    def is_completed(self, session_id: str, user_id: int | None = None) -> bool:
        session = self.get_session(session_id, user_id)
        if not session:
            raise ValueError("Interview session not found.")
        return session["is_completed"] or len(session["history"]) >= session["total_questions"]

    def get_history(self, session_id: str, user_id: int | None = None) -> list[InterviewHistoryItem]:
        session = self.get_session(session_id, user_id)
        if not session:
            raise ValueError("Interview session not found.")
        return session["history"]

    def get_average_score(self, session_id: str, user_id: int | None = None) -> int:
        session = self.get_session(session_id, user_id)
        if not session:
            raise ValueError("Interview session not found.")
        return session["average_score"]


session_manager = SessionManager()
