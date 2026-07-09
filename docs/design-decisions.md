# AI Job Copilot - Design Decisions

## Why FastAPI?
High performance, automatic validation, async support and OpenAPI generation.

## Why Service Layer?
Keeps API routes thin and business logic reusable.

## Why LLMService?
Provider abstraction. Switching between Groq, OpenAI or Hugging Face requires minimal changes.

## Why RAG?
Uses resume context instead of relying only on the LLM's internal knowledge.

## Why ChromaDB?
Purpose-built vector database for semantic search.

## Why ChatPromptTemplate?
Supports chat models with clear separation of system and user instructions.

## Why PydanticOutputParser?
Guarantees structured, validated outputs without manual JSON parsing.

## Why Session Manager?
Separates interview state management from business logic and enables future migration to MongoDB.

## Why MongoDB (Future)?
Interview sessions, reports and AI-generated documents naturally fit a document database.

## Why Adaptive Interviews?
Each new question depends on previous answers, making interviews more realistic than static questionnaires.
