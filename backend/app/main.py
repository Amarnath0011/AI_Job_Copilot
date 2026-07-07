from fastapi import FastAPI
from app.api.resume import router as resume_router

app = FastAPI(
    title="AI Job Copilot",
    version="1.0.0"
)

app.include_router(resume_router)


@app.get("/")
def root():
    return {"message": "Welcome to AI Job Copilot 🚀"}


@app.get("/health")
def health():
    return {"status": "OK"}