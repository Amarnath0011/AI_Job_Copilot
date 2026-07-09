# AI Job Copilot - Engine Design

# Resume Engine
Purpose:
Process uploaded resumes into searchable knowledge.

Workflow

```text
Upload PDF
    ↓
PDF Parser
    ↓
Extract Text
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
```

Responsibilities
- Upload handling
- Parsing
- Chunking
- Metadata generation
- Storage

---

# ATS Engine

Purpose:
Evaluate how well a resume matches a Job Description.

Workflow

```text
Job Description
        +
Resume Context
        ↓
Retriever
        ↓
Similarity Engine
        ↓
Keyword Engine
        ↓
Prompt Builder
        ↓
LLM
        ↓
ATS Report
```

Responsibilities
- Semantic similarity
- Keyword matching
- Missing skills
- AI feedback

---

# Interview Engine

Purpose:
Generate adaptive interviews.

Workflow

```text
Start Interview
      ↓
Generate Question
      ↓
Candidate Answer
      ↓
Evaluate Answer
      ↓
Generate Next Question
      ↓
Final Report
```

Responsibilities
- Question generation
- Answer evaluation
- Session history
- Adaptive questioning
- Interview report

---

# LLM Engine

Purpose:
Provide a single abstraction over multiple providers.

Responsibilities
- Provider abstraction
- Prompt execution
- Response generation

Current:
- Groq
- Llama 3.1 8B Instant

Future:
- OpenAI
- Hugging Face
- OpenRouter
- Gemini

---

# Prompt Engine

Purpose:
Create structured prompts using ChatPromptTemplate.

Responsibilities
- System prompts
- Human prompts
- Output formatting
- Prompt reuse

---

# Parser Engine

Purpose:
Convert raw LLM output into validated Pydantic models.

Responsibilities
- Structured output
- Validation
- Parsing

---

# Session Engine

Purpose:
Maintain interview state.

Stores
- Resume Context
- Job Description
- Current Question
- History
- Scores
- Final Report
