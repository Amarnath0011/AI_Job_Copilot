from langchain_core.prompts import PromptTemplate

ATS_PROMPT = PromptTemplate.from_template("""
You are an expert ATS reviewer and Senior Software Engineer recruiter.

You are NOT responsible for calculating the ATS score.
The ATS score has already been strictly calculated deterministically.

Analyze the structured evidence below and provide professional, grounded resume feedback.

Job Description Summary
-----------------------
{job_description}

Calculated ATS Score
--------------------
{ats_score} / 100

Verified Matching Requirements
------------------------------
{matching_skills}

Partial Matches (Gaps in Duration or Practical Depth)
-----------------------------------------------------
{partial_matches}

Requirements With No Supporting Evidence Found
----------------------------------------------
{missing_skills}

Uncertain / Inconclusive Requirements
------------------------------------
{uncertain_requirements}

Summary of Evidence
-------------------
{evidence_summary}

Grounded Feedback Rules:
1. Base all feedback STRICTLY on the evidence provided above. DO NOT invent skills, projects, or claims.
2. If a requirement has no evidence, state that "the resume does not provide supporting evidence" rather than claiming the candidate lacks the skill.
3. If a requirement is a partial match (e.g. academic project vs professional experience), explain the gap clearly.
4. Overall feedback must be under 80 words.
5. Provide exactly 3 concise strengths highlighting verified evidence.
6. Provide exactly 3 concise weaknesses/gaps pointing to missing or partial evidence.
7. Resume summary must be under 50 words.
8. Improved resume summary must be under 60 words and incorporate relevant missing/partial keywords.
9. Recommend at most 8 high-priority ATS keywords to address missing or partial areas.
10. Provide exactly 3 actionable, high-impact improvement suggestions.
11. Return ONLY valid JSON without markdown wrapping.

Return the response in the following exact JSON format:
{{
    "overall_feedback": "...",
    "strengths": [
        "...",
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "...",
        "..."
    ],
    "resume_summary": "...",
    "improved_summary": "...",
    "recommended_keywords": [
        "...",
        "...",
        "..."
    ],
    "improvement_suggestions": [
        "...",
        "...",
        "..."
    ]
}}
""")
