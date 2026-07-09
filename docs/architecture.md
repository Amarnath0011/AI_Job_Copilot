# AI Job Copilot - Architecture

## High Level Architecture

```text
                User
                  │
                  ▼
         React Dashboard / Chrome Extension
                  │
                  ▼
              FastAPI API Layer
                  │
      ┌───────────┼────────────┐
      ▼           ▼            ▼
 Resume Engine  ATS Engine  Interview Engine
      │           │            │
      └───────────┼────────────┘
                  ▼
             LLM Service
                  │
                  ▼
          Groq / Future Providers
                  │
                  ▼
       Structured Pydantic Output
```

## Layers

### API Layer
Receives HTTP requests, validates data using Pydantic models and delegates business logic to services.

### Service Layer
Contains business logic. Services orchestrate retrieval, prompting, LLM invocation and parsing.

### AI Layer
Contains prompt templates, embedding model and provider abstraction.

### RAG Layer
Responsible for chunking, embeddings, vector storage and semantic retrieval.

### Storage Layer
Current:
- ChromaDB (vector storage)
- Local uploads

Future:
- MongoDB (application data)
