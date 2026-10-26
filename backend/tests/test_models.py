from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models import InterviewSession, Resume, User


def test_resume_and_interview_session_models_are_user_scoped():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)

    with TestSession() as db:
        first_user = User(name="First User", email="first@example.com", password_hash="hash-1")
        second_user = User(name="Second User", email="second@example.com", password_hash="hash-2")
        db.add_all([first_user, second_user])
        db.commit()

        resume_id = str(uuid4())
        resume = Resume(
            id=resume_id,
            session_id=str(uuid4()),
            user_id=first_user.id,
            original_filename="resume.pdf",
            cloudinary_url="https://example.invalid/private-resume",
            cloudinary_public_id="private/resume",
            extracted_text="Python FastAPI SQLAlchemy",
        )
        db.add(resume)
        db.commit()

        interview = InterviewSession(
            id=str(uuid4()),
            user_id=first_user.id,
            resume_id=resume.id,
            job_description="Backend engineer role with Python and SQL",
            resume_context="Python FastAPI SQLAlchemy",
            current_question="Explain dependency injection in FastAPI.",
            total_questions=5,
            history=[],
        )
        db.add(interview)
        db.commit()

        assert db.query(Resume).filter(Resume.user_id == first_user.id).count() == 1
        assert db.query(Resume).filter(Resume.user_id == second_user.id).count() == 0
        assert db.query(InterviewSession).filter(InterviewSession.user_id == first_user.id).count() == 1
        assert db.query(InterviewSession).filter(InterviewSession.user_id == second_user.id).count() == 0

        # Compatibility aliases keep the existing users table field names.
        assert first_user.full_name == "First User"
        assert first_user.hashed_password == "hash-1"
