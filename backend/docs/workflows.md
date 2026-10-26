# AI Job Copilot - Workflows

## Resume Upload

```text
Upload
 ↓
Parse PDF
 ↓
Extract Text
 ↓
Split Text
 ↓
Embeddings
 ↓
ChromaDB
```

## ATS Analysis

```text
Job Description
 ↓
Retriever
 ↓
Resume Context
 ↓
Similarity
 ↓
Keyword Matching
 ↓
Prompt
 ↓
LLM
 ↓
Structured Output
```

## Interview Question Generation

```text
Resume
+
JD
 ↓
Retriever
 ↓
Prompt
 ↓
LLM
 ↓
Pydantic Parser
 ↓
Questions
```

## Answer Evaluation

```text
Question
+
Answer
 ↓
Prompt
 ↓
LLM
 ↓
Pydantic Parser
 ↓
Evaluation
```

## Mock Interview

```text
Start
 ↓
Generate Question
 ↓
Answer
 ↓
Evaluate
 ↓
Next Question
 ↓
Interview Report
```
