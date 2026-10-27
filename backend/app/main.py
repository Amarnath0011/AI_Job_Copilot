from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.ats import router as ats_router
from app.api.interview import router as interview_router
from app.api.test import router as test_router
from app.api.test2 import router as test2_router
from app.api.deps import get_current_user
from app.core.config import DATABASE_URL
from app.db.base import Base
from app.db.database import engine
from app.db import models  # noqa: F401 - register SQLAlchemy models
from app.db.models import User
from app.rag.retriever import get_retriever


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Creates only missing tables; it does not drop or rewrite the existing users table.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="AI Job Copilot", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(ats_router)
app.include_router(interview_router)
app.include_router(test_router)
app.include_router(test2_router)


@app.get("/")
def root():
    return {"message": "Welcome to AI Job Copilot 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(query: str, current_user: User = Depends(get_current_user)):
    retriever = get_retriever(document_type="resume", user_id=current_user.id, k=5)
    docs = retriever.invoke(query)
    return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
