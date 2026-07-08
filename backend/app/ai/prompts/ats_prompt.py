from langchain_core.prompts import PromptTemplate



ATS_PROMPT = PromptTemplate.from_template("""
You are an expert ATS reviewer and Senior Software Engineer recruiter.

You are NOT responsible for calculating the ATS score.
The ATS score has already been calculated.

Analyze the information below and provide professional resume feedback.

Resume
-------
{resume}

Job Description
---------------
{job_description}

ATS Score
---------
{ats_score}

Matching Skills
---------------
{matching_skills}

Missing Skills
--------------
{missing_skills}

Return ONLY valid JSON in the following format:

{{
    "overall_feedback": "...",
    "strengths": [
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "..."
    ],
    "resume_summary": "...",
    "improved_summary": "...",
    "recommended_keywords": [
        "...",
        "..."
    ],
    "improvement_suggestions": [
        "...",
        "..."
    ]
}}

Do not return markdown.
Do not return explanations outside JSON.
""")

