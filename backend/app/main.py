from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.resume import router as resume_router
from app.api.ats import router as ats_router
from app.api.interview import router as interview_router
from app.api.test import router as test_router
from app.api.test2 import router as test2_router

from app.rag.retriever import get_retriever
from app.api.resume import router

app = FastAPI(
    title="AI Job Copilot",
    version="1.0.0",
)

# Routers
app.include_router(resume_router)
app.include_router(ats_router)
app.include_router(interview_router)
app.include_router(test_router)
app.include_router(test2_router)


@router.get("/search")
def search(query: str):

    retriever = get_retriever()

    docs = retriever.invoke(query)

    return [
        {
            "content": d.page_content,
            "metadata": d.metadata,
        }
        for d in docs
    ]


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Job Copilot 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)