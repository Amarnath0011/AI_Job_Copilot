from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.ats import router as ats_router
from app.api.interview import router as interview_router
from app.api.test import router as test_router
from app.api.test2 import router as test2_router
from app.db.database import Base, engine
from app.db import models  # noqa: F401 - register SQLAlchemy models


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="AI Job Copilot", version="1.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
