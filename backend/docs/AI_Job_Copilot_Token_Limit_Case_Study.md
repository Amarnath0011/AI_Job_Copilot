# AI Job Copilot -- Engineering Challenge: LLM Token Limit During Interview Report Generation

## Background

While building the **AI Job Copilot** backend, one of the most
interesting engineering challenges appeared during **Milestone 5.4 -- AI
Interview Report Generation**.

The goal of this feature was to generate a final interview report after
a candidate completed an adaptive interview.

The architecture was:

``` text
Interview Session
        ↓
Questions
        ↓
Candidate Answers
        ↓
Answer Evaluation
        ↓
Interview Report Prompt
        ↓
Groq (Llama 3.1 8B Instant)
        ↓
PydanticOutputParser
        ↓
InterviewReportResponse
```

The implementation itself was correct, but the request repeatedly failed
with a runtime error.

------------------------------------------------------------------------

# Problem

The Groq API returned:

    413 Request Too Large

    Request too large for model llama-3.1-8b-instant

    Limit : 6000 TPM

    Requested : 6558 Tokens

Initially, it looked like an API limitation, but after investigating the
prompt and payload, the real issue was prompt design.

------------------------------------------------------------------------

# Root Cause Analysis

The report generation prompt was sending all available information to
the LLM.

The payload contained:

-   Resume Context (RAG)
-   Job Description
-   Interview History
-   Candidate Answers
-   Question-wise Evaluations
-   System Prompt
-   Pydantic Format Instructions

This caused the request to exceed the model's token limit.

------------------------------------------------------------------------

# Why Was This Happening?

The biggest contributor was duplicated information.

For every interview question, we were sending:

Question

↓

Candidate Answer

↓

LLM Evaluation

However, the evaluation was already generated **from the answer**.

That means the model received the same information twice.

Example:

Question: Explain HashMap.

Answer: (HashMap explanation...)

Evaluation:

-   Score: 82
-   Feedback
-   Strengths
-   Weaknesses

The evaluation already summarized the answer.

Sending the raw answer again added hundreds of unnecessary tokens.

------------------------------------------------------------------------

# Options Considered

## Option 1 -- Upgrade the LLM Plan

Increase the Groq token limit.

### Pros

-   No code changes.

### Cons

-   Does not solve the engineering problem.
-   Higher cost.
-   Still fails for longer interviews.
-   Not scalable.

Decision: Rejected.

------------------------------------------------------------------------

## Option 2 -- Remove Interview History Completely

Only send resume and evaluations.

### Pros

-   Large token reduction.

### Cons

-   The report loses chronological interview flow.
-   The LLM cannot easily understand progression during the interview.
-   Less explainable report.

Decision: Rejected.

------------------------------------------------------------------------

## Option 3 -- Keep Everything and Hope Prompt Compression Helps

Reduce only the wording of the system prompt.

### Pros

-   Very small implementation effort.

### Cons

-   Saves only a few hundred tokens.
-   The payload remains too large.
-   Does not address duplicated context.

Decision: Rejected.

------------------------------------------------------------------------

## Option 4 -- Summarize Interview Context (Chosen Solution)

Keep the interview history, but replace verbose candidate answers with
compact evaluation summaries.

Instead of sending:

Question

↓

Answer

↓

Evaluation

Send:

Question

↓

Score

↓

Feedback

↓

Strengths

↓

Weaknesses

The evaluation already captures the important information from the
answer.

This removes redundancy while preserving the interview timeline.

Decision: Selected.

------------------------------------------------------------------------

# Why This Solution?

It follows an important GenAI engineering principle:

> Downstream LLMs should consume structured summaries instead of
> repeatedly processing the original raw context.

Benefits:

-   Significant token reduction.
-   Lower inference cost.
-   Faster responses.
-   Better scalability.
-   Preserves report quality.
-   Keeps the existing architecture unchanged.

No service refactoring is required.

Only the prompt context becomes more efficient.

------------------------------------------------------------------------

# Additional Optimizations

Along with compact interview history:

-   Retrieve fewer resume chunks for report generation.
-   Shorten repetitive system prompt instructions.
-   Replace verbose JSON dumps with compact textual summaries.
-   Keep structured outputs through PydanticOutputParser and
    OutputFixingParser.

------------------------------------------------------------------------

# Final Design

``` text
Resume Context (Top Relevant Chunks)
            +
Job Description
            +
Compressed Interview History
            +
Structured Format Instructions
            ↓
Groq Llama 3.1
            ↓
Structured Interview Report
```

------------------------------------------------------------------------

# Interview Answer (2--3 Minutes)

One engineering challenge I faced was during the implementation of the
final interview report generation.

Initially, I sent the resume, job description, complete interview
history, raw candidate answers, and answer evaluations to the LLM.
Although the implementation was functionally correct, the request
exceeded Groq's token limit and returned a 413 "Request Too Large"
error.

After analyzing the payload, I realized that the raw answers and their
evaluations contained largely overlapping information. Since the
evaluations were already structured summaries generated from the
answers, sending both was redundant.

Instead of upgrading the API plan or removing interview history
entirely, I redesigned the prompt context. I kept the interview timeline
but replaced verbose answers with compact evaluation summaries that
included the score, strengths, weaknesses, and feedback.

This reduced the token usage significantly while preserving report
quality. It also improved scalability, reduced inference cost, and
required no changes to the existing service architecture.

This experience taught me that in GenAI systems, prompt engineering and
context optimization are as important as the application code itself.


//Some more problems i solved during the interview_report_generation 

1. Token Limit Exceeded (413)

Problem:
While generating the final interview report, the LLM returned a 413 Request Too Large error because the prompt exceeded the model's token limit.

Root Cause:
I was sending the resume, job description, complete interview history, raw answers, and detailed evaluations together, creating a very large prompt.

Solution:
I compressed the interview history by removing raw answers and keeping only evaluation summaries, which significantly reduced token usage without changing the architecture.

2. Duplicate Context

Problem:
The same information was being sent to the LLM multiple times, increasing token usage unnecessarily.

Root Cause:
Both the candidate's raw answers and their AI-generated evaluations were included, even though the evaluations already summarized the answers.

Solution:
I redesigned the prompt to use only the compressed evaluation summaries, eliminating redundant context and improving efficiency.

3. Parser Returning JSON Schema ($defs)

Problem:
The LLM returned the Pydantic JSON schema ($defs, properties, etc.) instead of actual data.

Root Cause:
The smaller Llama 3.1 8B model misinterpreted the parser's format instructions and echoed the schema.

Solution:
I strengthened the prompt with explicit instructions to return only JSON values and never include schema-related fields like $defs or properties.

4. Nested Pydantic Parsing

Problem:
The parser frequently failed when parsing nested objects such as QuestionFeedback.

Root Cause:
Nested schemas made the output format more complex, increasing the chance of incorrect JSON generation by the LLM.

Solution:
I simplified the response structure where possible and refined the prompt so the model consistently generated valid nested JSON.

5. Output Truncation

Problem:
The generated interview report was incomplete, causing JSON parsing failures.

Root Cause:
The response was too long because the report contained detailed feedback, long summaries, and ideal answers for every question.

Solution:
I reduced unnecessary output, shortened prompts, and optimized the response structure so the model could finish generating valid JSON.

6. Session Lifecycle Bugs

Problem:
The interview session became unavailable after generating the final report.

Root Cause:
The session was being deleted immediately after report generation, making repeated access impossible during testing.

Solution:
I modified the session lifecycle so reports could be generated successfully while keeping the architecture ready for future MongoDB persistence.

7. Prompt Optimization

Problem:
The AI sometimes generated repetitive questions or unrealistic evaluation scores.

Root Cause:
The prompts were too generic and lacked strict evaluation rules, relevance checks, and clear scoring guidelines.

Solution:
I redesigned the prompts with explicit scoring rubrics, relevance-based evaluation, adaptive difficulty, and concise context, resulting in more realistic and consistent outputs.
