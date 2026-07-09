# AI Job Copilot 🚀

An AI-powered career assistant that helps candidates optimize their resumes, evaluate ATS compatibility, prepare for interviews, and streamline job applications using Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), and semantic search.

---

# Overview

AI Job Copilot is a full-stack AI application designed to assist job seekers throughout the hiring process.

The application allows users to upload their resumes, compare them against job descriptions, receive ATS scores, identify missing skills, generate AI-powered resume improvements, prepare personalized interview questions, and eventually interact with an AI interviewer.

The project is built using a production-oriented architecture powered by FastAPI, LangChain, ChromaDB, and Large Language Models. The LLM layer is abstracted through a dedicated `LLMService`, allowing seamless switching between providers (Groq, OpenAI, Hugging Face, OpenRouter, etc.) with minimal code changes. A React dashboard and Chrome Extension are planned for the frontend.

---

# Why AI Job Copilot?

Most AI resume tools focus on a single task such as ATS scoring or resume feedback.

AI Job Copilot provides an end-to-end AI-powered job preparation platform that assists candidates throughout the hiring journey—from resume optimization and ATS analysis to personalized interview preparation, answer evaluation, and eventually mock interviews and browser-based job application assistance.

The project is designed with a modular, production-oriented backend architecture that enables easy integration of new AI features and LLM providers.



# Features

## ✅ Resume Upload

* Upload PDF resume
* Store securely
* Extract text
* Parse document

---

## ✅ Resume Processing

* PDF parsing
* Text extraction
* Chunking using RecursiveCharacterTextSplitter
* Metadata generation

---

## ✅ Vector Database

* Hugging Face Embeddings
* ChromaDB
* Semantic Search
* Metadata filtering

---

## ✅ ATS Analysis

* Resume vs Job Description comparison
* Semantic similarity scoring
* Keyword matching
* Missing skills detection
* Matching skills detection

---

## ✅ AI Resume Improvement

* AI resume feedback
* Resume enhancement suggestions
* ATS optimization recommendations
* Missing keyword suggestions

---

## ✅ AI Interview Preparation

* Personalized Technical Questions
* Behavioral Questions
* HR Questions
* Project-based Questions
* Resume-aware Question Generation
* Job Description-aware Questions

---

## 🚧 AI Mock Interview

* Candidate answers
* AI evaluation
* Feedback
* Follow-up questions
* Performance scoring

---

## 🚧 AI Answer Evaluation

* Evaluate candidate answers
* AI-generated feedback
* Technical scoring
* Communication scoring
* Improvement suggestions

---

## 🚧 Voice Interview

* Speech-to-text
* AI interviewer
* Spoken responses
* Voice feedback

---

## 🚧 Chrome Extension

Automatically detects job postings on:

* LinkedIn
* Careers Page
* Company Job Portals

Then:

* Extract Job Description
* Calculate ATS Match
* Show Missing Skills
* Generate Interview Questions
* One-click Preparation

---

# Tech Stack

## Backend

* Python
* FastAPI
* Uvicorn

---

## AI

* LangChain
* Groq API
* Llama 3.1 8B Instant
* Prompt Engineering
* LangChain PromptTemplate
* Retrieval-Augmented Generation (RAG)

---

## Embeddings

* HuggingFaceEmbeddings
* all-MiniLM-L6-v2

---

## Vector Database

* ChromaDB

---

## Frontend (Planned)

* React
* Tailwind CSS
* Axios

---

## Database (Future)

* PostgreSQL 

---

## Browser Extension

* JavaScript
* Chrome Extension Manifest V3

---

# System Architecture

```text
                      User
                       │
                       ▼
                 Upload Resume
                       │
                       ▼
                  FastAPI API
                       │
                       ▼
                  PDF Parser
                       │
                       ▼
                Text Extraction
                       │
                       ▼
                 Text Chunking
                       │
                       ▼
              Embedding Model
                       │
                       ▼
                  ChromaDB
                       │
                       ▼
                 RAG Retriever
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   ATS Service   Interview Service   Future Company Service
        │              │
        ▼              ▼
   Prompt Builder  Prompt Builder
        │              │
        └───────┬──────┘
                ▼
           LLM Service
                │
                ▼
         Groq (Llama 3.1)
                │
                ▼
         Structured JSON
                │
                ▼
          API Response
```

---

# Project Structure

```text
backend/
└── app/
    ├── ai/
    │   ├── llm.py
    │   ├── embeddings.py
    │   └── prompts/
    │       ├── ats_prompt.py
    │       ├── interview.py
    │       └── company.py
    │
    ├── api/
    │   ├── resume.py
    │   ├── ats.py
    │   ├── interview.py
    │   └── test.py
    │
    ├── ats/
    │   ├── scorer.py
    │   └── analyzer.py
    │
    ├── core/
    │   └── config.py
    │
    ├── models/
    │   ├── ats_models.py
    │   ├── interview_models.py
    │   └── llm_models.py
    │
    ├── rag/
    │   ├── splitter.py
    │   ├── vector_store.py
    │   ├── retriever.py
    │   └── document_store.py
    │
    ├── services/
    │   ├── resume_service.py
    │   ├── ats_service.py
    │   ├── interview_service.py
    │   ├── llm_service.py
    │   ├── keyword_service.py
    │   ├── similarity_service.py
    │   └── parser.py
    │
    ├── utils/
    │   └── session.py
    │
    ├── uploads/
    │
    └── main.py
```

---

# Current API Endpoints

## Resume

| Method | Endpoint         | Description   |
| ------ | ---------------- | ------------- |
| POST   | `/resume/upload` | Upload Resume |

---

## ATS

| Method | Endpoint       | Description                        |
| ------ | -------------- | ---------------------------------- |
| POST   | `/ats/analyze` | Resume vs Job Description Analysis |
| POST   | `/interview/analyze` | Resume vs Job Description Analysis |

---

## Testing

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/test/llm`        | Test LLM Connection |
| GET    | `/test/ats-prompt` | Test ATS Prompt     |

---

# Current Workflow

```text
Resume Upload
        │
        ▼
PDF Parsing
        │
        ▼
Chunking
        │
        ▼
Embeddings
        │
        ▼
ChromaDB
        │
        ▼
Retriever (RAG)
        │
        ▼
Resume Context
        │
        ▼
Prompt Engineering
        │
        ▼
LLM Service
        │
        ▼
Groq (Llama 3.1)
        │
        ▼
Structured JSON Response
```

---

# Future Roadmap

## Phase 1 ✅
* FastAPI Setup
* Resume Upload
* PDF Parsing
* Text Extraction
* Chunking
* Embeddings
* ChromaDB
* Semantic Retrieval

## Phase 2 ✅
* ATS Scoring
* Keyword Matching
* Semantic Similarity
* Missing Skills Detection

## Phase 3 ✅
* AI Resume Feedback
* Resume Improvement Suggestions

## Phase 4 ✅
* Personalized Interview Question Generator

## Phase 5 🚧
* AI Answer Evaluation
* Interactive Mock Interview
* Follow-up Questions

## Phase 6
* Company-specific Interview Coach

## Phase 7
* Voice Interview

## Phase 8
* Chrome Extension

## Phase 9
* React Dashboard

## Phase 10
* Deployment
---

# Setup

```bash
git clone <repository>

cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

# Environment Variables

```env
HF_TOKEN=your_huggingface_token

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

# Skills Demonstrated

* Large Language Models (LLMs)
* Groq API
* AI Interview Systems
* Prompt Engineering
* Retrieval-Augmented Generation (RAG)
* Service Layer Architecture
* Dependency Injection (if applicable)
* Modular Backend Design
* Production-grade API Development
---

# Author

**Amarnath**

MCA, NIT Jamshedpur

AI Engineer | Backend Developer | GenAI Enthusiast
