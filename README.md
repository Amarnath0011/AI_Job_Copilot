# AI Job Copilot 🚀

An AI-powered career assistant that helps candidates optimize their resumes, evaluate ATS compatibility, prepare for interviews, and streamline job applications using Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), and semantic search.

---

# Overview

AI Job Copilot is a full-stack AI application designed to assist job seekers throughout the hiring process.

The application allows users to upload their resumes, compare them against job descriptions, receive ATS scores, identify missing skills, generate AI-powered resume improvements, prepare personalized interview questions, and eventually interact with an AI interviewer.

The project is being built with a production-oriented architecture using FastAPI, LangChain, Hugging Face models, ChromaDB, and a React frontend.

---

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

## 🚧 AI Resume Improvement

* Resume feedback
* Resume summary improvement
* ATS improvement suggestions
* Keyword recommendations

---

## 🚧 Interview Preparation

* Technical Questions
* Behavioral Questions
* HR Questions
* Project-based Questions

---

## 🚧 AI Mock Interview

* Candidate answers
* AI evaluation
* Feedback
* Follow-up questions
* Performance scoring

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
* Hugging Face Inference API
* Qwen 2.5 7B Instruct
* PromptTemplate

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

         Hugging Face Embeddings

                    │

                    ▼

                ChromaDB

                    │

                    ▼

               RAG Retriever

                    │

      ┌─────────────┴──────────────┐

      ▼                            ▼

 ATS Scorer                 AI Analyzer

      ▼                            ▼

Similarity              Hugging Face LLM

Keyword Match                  Prompt

      ▼                            ▼

      └─────────────┬──────────────┘

                    ▼

              Final ATS Report
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

↓

Text Extraction

↓

Chunking

↓

Embeddings

↓

ChromaDB

↓

Retriever

↓

ATS Score

↓

LLM Feedback

↓

JSON Response
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

---

## Phase 2 ✅

* ATS Scoring
* Similarity Matching
* Keyword Matching

---

## Phase 3 🚧

* Resume Improvement
* AI Feedback

---

## Phase 4

* Interview Question Generator

---

## Phase 5

* Mock Interview

---

## Phase 6

* Voice Interview

---

## Phase 7

* Chrome Extension

---

## Phase 8

* React Dashboard

---

## Phase 9

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

* FastAPI
* REST APIs
* Retrieval-Augmented Generation (RAG)
* Prompt Engineering
* Semantic Search
* Vector Databases
* ChromaDB
* Hugging Face Inference API
* Hugging Face Embeddings
* LangChain
* AI Application Development
* Backend Architecture
* Production-oriented Project Structure

---

# Author

**Amarnath**

MCA, NIT Jamshedpur

AI Engineer | Backend Developer | GenAI Enthusiast
