from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.models.interview_models import (
    InterviewEvaluationResponse,
    InterviewQuestionResponse,
)

# ==========================================================
# Interview Question Generation
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

Your task is to generate personalized interview questions.

Guidelines:

1. Analyze the resume and the job description carefully.
2. Prioritize technologies common to both.
3. Generate project-based questions whenever possible.
4. Start with easier questions and gradually increase the difficulty.
5. Avoid generic textbook questions.
6. Behavioral questions should assess teamwork, ownership, leadership and communication.
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
# Interview Answer Evaluation
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

Scoring Rubric:

1. Technical Accuracy (40%)
2. Completeness (25%)
3. Communication (15%)
4. Best Practices (20%)

Evaluation Rules:

- Be fair and constructive.
- Explain why marks were deducted.
- Highlight strengths.
- Suggest improvements.
- Provide an ideal answer.
- Scores must be between 0 and 100.

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