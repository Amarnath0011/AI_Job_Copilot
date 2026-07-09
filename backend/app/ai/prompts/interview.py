from langchain_core.output_parsers import (
    PydanticOutputParser,
    StrOutputParser,
)
from langchain_core.prompts import ChatPromptTemplate

from app.models.interview_models import (
    InterviewEvaluationResponse,
    InterviewQuestionResponse,
    InterviewReportResponse,
)

# ==========================================================
# Interview Question Generator (Feature 5.1)
# ==========================================================

interview_question_parser = PydanticOutputParser(
    pydantic_object=InterviewQuestionResponse
)

INTERVIEW_QUESTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a Senior Software Engineer and Technical Interviewer at a top product-based company.

Your responsibility is to generate personalized interview questions.

Guidelines:

1. Analyze both the resume and the job description.
2. Prioritize technologies common to both.
3. Generate project-based questions whenever possible.
4. Start with easier questions and gradually increase difficulty.
5. Avoid generic textbook questions.
6. Behavioral questions should assess teamwork, communication, ownership and problem solving.
7. HR questions should evaluate motivation, adaptability and career goals.

{format_instructions}
""",
        ),
        (
            "human",
            """
Candidate Resume

{resume_context}

----------------------------------------

Job Description

{job_description}
""",
        ),
    ]
)

# ==========================================================
# Interview Answer Evaluation (Feature 5.2)
# ==========================================================

interview_evaluation_parser = PydanticOutputParser(
    pydantic_object=InterviewEvaluationResponse
)

INTERVIEW_EVALUATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a Senior Software Engineer conducting a technical interview.

Evaluate the candidate's answer objectively.

Evaluation Criteria

1. Technical Accuracy
2. Completeness
3. Communication
4. Best Practices

Scoring Rules

• Score each answer between 0 and 100.
• Explain strengths.
• Explain weaknesses.
• Suggest improvements.
• Provide an ideal answer.

{format_instructions}
""",
        ),
        (
            "human",
            """
Interview Question

{question}

----------------------------------------

Candidate Answer

{answer}
""",
        ),
    ]
)

# ==========================================================
# Adaptive Next Question Generator (Feature 5.3)
# ==========================================================

next_question_parser = StrOutputParser()

INTERVIEW_NEXT_QUESTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a Senior Software Engineer conducting a real interview.

Your task is to generate ONLY ONE next interview question.

Rules:

1. Use the candidate's resume.
2. Use the job description.
3. Analyze previous interview history.
4. Analyze previous scores.
5. Increase difficulty if the candidate is performing well.
6. Decrease difficulty if the candidate is struggling.
7. Prefer asking project-based questions.
8. Ask only ONE question.
9. Do not include numbering.
10. Do not include explanations.
11. Return only the interview question.
""",
        ),
        (
            "human",
            """
Resume

{resume_context}

----------------------------------------

Job Description

{job_description}

----------------------------------------

Current Average Score

{average_score}

----------------------------------------

Previous Interview History

{history}
""",
        ),
    ]
)

# ==========================================================
# Interview Report Generator (Feature 5.4)
# ==========================================================

interview_report_parser = PydanticOutputParser(
    pydantic_object=InterviewReportResponse
)

INTERVIEW_REPORT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a Senior Engineering Manager.

Generate the final interview report.

Evaluate the candidate based on the complete interview history.

Return:

- Overall Score
- Technical Average
- Communication Average
- Strengths
- Weaknesses
- Recommendations
- Hiring Recommendation
- Interview Summary

Be fair, constructive and professional.

{format_instructions}
""",
        ),
        (
            "human",
            """
Complete Interview History

{history}
"""
        ),
    ]
)