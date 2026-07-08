from fastapi import FastAPI
from app.api.resume import router as resume_router
from app.rag.retriever import get_retriever
from app.api.resume import router
from app.api.ats import router as ats_router
from app.api.test import router as test_router
from app.api.test2 import router as test2_router

app = FastAPI(
    title="AI Job Copilot",
    version="1.0.0"
)

app.include_router(resume_router)
app.include_router(ats_router)

@router.get("/search")
def search(query: str):

    retriever = get_retriever()

    docs = retriever.invoke(query)

    return [
        {
            "content": d.page_content,
            "metadata": d.metadata
        }
        for d in docs
    ]

@app.get("/")
def root():
    return {"message": "Welcome to AI Job Copilot 🚀"}


@app.get("/health")
def health():
    return {"status": "OK"}