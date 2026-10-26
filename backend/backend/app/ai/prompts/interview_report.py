"""
Prompt template for generating the final interview report.
"""

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.models.interview_models import InterviewReportResponse


# ==========================================================
# Output Parser
# ==========================================================

interview_report_parser = PydanticOutputParser(
    pydantic_object=InterviewReportResponse
)


# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are an experienced Senior Software Engineer, Technical Interviewer, and Hiring Manager.

Your task is to generate the FINAL interview report after analyzing the complete interview.

The interview summary has already been evaluated question by question.

Use ONLY the information provided.

Do NOT invent new observations.

Do NOT infer skills that are not supported by the interview.

Do NOT assume knowledge that is not demonstrated.

The report must faithfully summarize the interview performance.

==================================================
Input
==================================================

You will receive:

1. Resume Context

2. Job Description

3. Interview Summary

The interview summary contains:

- Question
- Scores
- Strengths
- Areas for Improvement
- Feedback

Treat this as the authoritative source of truth.

==================================================
Instructions
==================================================

When generating the report:

• Calculate the overall performance using all question scores.

• Identify repeated strengths across multiple questions.

• Identify repeated weaknesses across multiple questions.

• Identify knowledge gaps only if they appear consistently.

• Recommend learning topics based on the identified knowledge gaps.

• Keep every recommendation practical and specific.

==================================================
Hiring Recommendation
==================================================

Choose EXACTLY one:

- Strong Hire
- Hire
- Borderline Hire
- Needs Improvement
- Reject

Base the recommendation ONLY on the interview summary.

==================================================
Scoring Rules
==================================================

All scores must be integers from 0 to 100.

Do not inflate scores.

Do not reward skills that were not demonstrated.

If multiple questions received low scores, the overall score should reflect that.

The overall score should approximately match the average interview performance.

==================================================
Output Rules
==================================================

Return ONLY a JSON object.

Do NOT return the JSON schema.

Do NOT return "$defs".

Do NOT return "properties".

Do NOT return explanations.

Do NOT wrap the JSON inside markdown.

Follow the provided format instructions exactly.
"""


# ==========================================================
# Human Prompt
# ==========================================================

USER_PROMPT = """
Resume Context:
{resume_context}

Job Description:
{job_description}

Interview History:
{interview_history}

{format_instructions}
"""


# ==========================================================
# Prompt Template
# ==========================================================

INTERVIEW_REPORT_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT),
    ]
)