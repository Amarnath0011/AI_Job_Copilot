from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.models.interview_models import InterviewQuestionResponse


# Parser
interview_question_parser = PydanticOutputParser(
    pydantic_object=InterviewQuestionResponse
)


# Prompt
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