import json
import logging
import re
from uuid import uuid4

from app.models.ats_models import JDRequirement
from app.services.keyword_service import KeywordService
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

# Catalog of known technical skills mapped to category and aliases
KNOWN_SKILLS_CATALOG: dict[str, dict] = {
    # Programming Languages
    "python": {"category": "programming_languages", "aliases": ["python 3", "python3", "py"]},
    "java": {"category": "programming_languages", "aliases": ["core java", "java 8", "java 11", "java 17", "java 21"]},
    "javascript": {"category": "programming_languages", "aliases": ["js", "es6", "ecmascript"]},
    "typescript": {"category": "programming_languages", "aliases": ["ts"]},
    "c++": {"category": "programming_languages", "aliases": ["cpp", "c plus plus"]},
    "c#": {"category": "programming_languages", "aliases": ["csharp", "c sharp", ".net"]},
    "c": {"category": "programming_languages", "aliases": ["c programming"]},
    "go": {"category": "programming_languages", "aliases": ["golang"]},
    "rust": {"category": "programming_languages", "aliases": []},
    "kotlin": {"category": "programming_languages", "aliases": []},
    "php": {"category": "programming_languages", "aliases": []},
    "ruby": {"category": "programming_languages", "aliases": ["ruby on rails"]},
    "scala": {"category": "programming_languages", "aliases": []},
    "swift": {"category": "programming_languages", "aliases": []},

    # Frameworks and Libraries
    "fastapi": {"category": "frameworks_libraries", "aliases": ["fast-api"]},
    "flask": {"category": "frameworks_libraries", "aliases": []},
    "django": {"category": "frameworks_libraries", "aliases": []},
    "react": {"category": "frameworks_libraries", "aliases": ["react.js", "reactjs"]},
    "redux": {"category": "frameworks_libraries", "aliases": ["redux toolkit"]},
    "next.js": {"category": "frameworks_libraries", "aliases": ["nextjs", "next js"]},
    "node": {"category": "frameworks_libraries", "aliases": ["node.js", "nodejs"]},
    "express": {"category": "frameworks_libraries", "aliases": ["express.js", "expressjs"]},
    "spring": {"category": "frameworks_libraries", "aliases": ["spring framework"]},
    "spring boot": {"category": "frameworks_libraries", "aliases": ["springboot"]},
    "hibernate": {"category": "frameworks_libraries", "aliases": []},
    "tailwind css": {"category": "frameworks_libraries", "aliases": ["tailwind", "tailwindcss"]},
    "bootstrap": {"category": "frameworks_libraries", "aliases": []},
    "tensorflow": {"category": "frameworks_libraries", "aliases": ["tf"]},
    "pytorch": {"category": "frameworks_libraries", "aliases": ["torch"]},
    "pandas": {"category": "frameworks_libraries", "aliases": []},
    "numpy": {"category": "frameworks_libraries", "aliases": []},
    "scikit-learn": {"category": "frameworks_libraries", "aliases": ["sklearn"]},
    "langchain": {"category": "frameworks_libraries", "aliases": []},
    "llamaindex": {"category": "frameworks_libraries", "aliases": ["llama-index"]},

    # Databases
    "sql": {"category": "databases", "aliases": ["structured query language"]},
    "mysql": {"category": "databases", "aliases": []},
    "postgresql": {"category": "databases", "aliases": ["postgres", "psql"]},
    "mongodb": {"category": "databases", "aliases": ["mongo"]},
    "redis": {"category": "databases", "aliases": []},
    "sqlite": {"category": "databases", "aliases": ["sqlite3"]},
    "elasticsearch": {"category": "databases", "aliases": ["elastic search"]},
    "chromadb": {"category": "databases", "aliases": ["chroma", "chroma db"]},
    "pinecone": {"category": "databases", "aliases": []},
    "faiss": {"category": "databases", "aliases": []},

    # APIs & Backend
    "rest": {"category": "apis_backend", "aliases": ["restful", "rest api", "restful api", "restful apis", "rest apis"]},
    "graphql": {"category": "apis_backend", "aliases": ["graph ql"]},
    "microservices": {"category": "apis_backend", "aliases": ["microservice", "microservice architecture"]},
    "grpc": {"category": "apis_backend", "aliases": ["g rpc"]},
    "rabbitmq": {"category": "apis_backend", "aliases": ["rabbit mq"]},
    "kafka": {"category": "apis_backend", "aliases": ["apache kafka"]},

    # Cloud & DevOps
    "docker": {"category": "cloud_devops", "aliases": ["containerization", "containers"]},
    "kubernetes": {"category": "cloud_devops", "aliases": ["k8s"]},
    "aws": {"category": "cloud_devops", "aliases": ["amazon web services"]},
    "azure": {"category": "cloud_devops", "aliases": ["microsoft azure"]},
    "gcp": {"category": "cloud_devops", "aliases": ["google cloud", "google cloud platform"]},
    "ci/cd": {"category": "cloud_devops", "aliases": ["continuous integration", "cicd"]},
    "github actions": {"category": "cloud_devops", "aliases": ["gh actions"]},
    "jenkins": {"category": "cloud_devops", "aliases": []},
    "terraform": {"category": "cloud_devops", "aliases": []},
    "git": {"category": "cloud_devops", "aliases": ["version control"]},
    "linux": {"category": "cloud_devops", "aliases": ["unix", "bash"]},

    # CS Fundamentals & DSA
    "data structures": {"category": "data_structures_algorithms", "aliases": ["dsa", "data structures and algorithms"]},
    "algorithms": {"category": "data_structures_algorithms", "aliases": ["algorithm design"]},
    "oop": {"category": "data_structures_algorithms", "aliases": ["object oriented programming", "oops"]},
    "system design": {"category": "data_structures_algorithms", "aliases": ["distributed systems", "high level design", "low level design"]},
    "dbms": {"category": "data_structures_algorithms", "aliases": ["database management"]},

    # Soft Skills
    "communication": {"category": "soft_skills", "aliases": ["communication skills", "verbal communication", "written communication"]},
    "teamwork": {"category": "soft_skills", "aliases": ["collaboration", "cross-functional collaboration"]},
    "problem solving": {"category": "soft_skills", "aliases": ["analytical skills", "critical thinking"]},
    "leadership": {"category": "soft_skills", "aliases": ["mentoring", "team lead"]},
}

# Regex patterns for experience, degree, and requirements
EXPERIENCE_PATTERNS = [
    re.compile(
        r"(?:at\s+least|minimum\s+of)?\s*(\d+(?:\.\d+)?)\+?\s*(?:to\s*\d+\s*)?(?:years?|yrs?)(?:\s*of)?\s*(?:hands-on\s+|professional\s+|work\s+)?experience\s*(?:in|with|using)?\s*([^,\.;\n]+)",
        re.IGNORECASE,
    ),
    re.compile(
        r"([^,\.;\n]+?)\s*experience\s*(?:of|for)?\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
        re.IGNORECASE,
    ),
]

EDUCATION_PATTERNS = [
    (re.compile(r"\b(?:bachelor'?s?|bs|ba|b\.?tech|b\.?e|undergraduate)\b(?:\s+degree)?(?:\s+in\s+([^,\.;\n]+))?", re.IGNORECASE), "Bachelor's Degree"),
    (re.compile(r"\b(?:master'?s?|ms|m\.?tech|m\.?e|mca|postgraduate)\b(?:\s+degree)?(?:\s+in\s+([^,\.;\n]+))?", re.IGNORECASE), "Master's Degree"),
    (re.compile(r"\b(?:ph\.?d|doctorate)\b(?:\s+in\s+([^,\.;\n]+))?", re.IGNORECASE), "Doctorate/PhD"),
]


class RequirementExtractor:
    """
    Extracts structured requirements from Job Descriptions.
    Combines deterministic keyword and pattern extraction with an optional LLM layer
    for semantic/contextual understanding, with robust fallback.
    """

    @classmethod
    def extract_deterministic(cls, job_description: str) -> list[JDRequirement]:
        """
        Deterministically extracts skills, education, and experience requirements from JD.
        """
        requirements: list[JDRequirement] = []
        seen_keys: set[str] = set()
        jd_lower = job_description.lower()

        # 1. Experience Requirements via regex
        for pattern in EXPERIENCE_PATTERNS:
            for match in pattern.finditer(job_description):
                groups = match.groups()
                if len(groups) == 2:
                    try:
                        # Depending on which pattern matched
                        if groups[0].replace(".", "", 1).isdigit():
                            years = float(groups[0])
                            topic = groups[1].strip()
                        else:
                            years = float(groups[1])
                            topic = groups[0].strip()
                    except ValueError:
                        continue

                    # Filter out overly long noise phrases
                    if len(topic) < 3 or len(topic) > 60:
                        continue

                    req_key = f"exp_{topic.lower()}"
                    if req_key not in seen_keys:
                        seen_keys.add(req_key)
                        req_id = f"req_{len(requirements) + 1}_{uuid4().hex[:6]}"
                        requirements.append(
                            JDRequirement(
                                requirement_id=req_id,
                                text=f"{int(years) if years.is_integer() else years}+ years of professional experience in {topic}",
                                normalized_name=topic.lower(),
                                category="professional_experience",
                                importance="critical" if years >= 3 else "high",
                                required_or_preferred="required",
                                weight=1.5 if years >= 3 else 1.2,
                                aliases=[f"{int(years) if years.is_integer() else years} years {topic}", topic.lower()],
                                years_required=years,
                            )
                        )

        # 2. Education Requirements
        for pattern, degree_name in EDUCATION_PATTERNS:
            match = pattern.search(job_description)
            if match:
                field = match.group(1).strip() if (match.lastindex and match.group(1)) else "Computer Science or related field"
                req_key = f"edu_{degree_name.lower()}"
                if req_key not in seen_keys:
                    seen_keys.add(req_key)
                    req_id = f"req_{len(requirements) + 1}_{uuid4().hex[:6]}"
                    requirements.append(
                        JDRequirement(
                            requirement_id=req_id,
                            text=f"{degree_name} in {field}",
                            normalized_name=degree_name.lower(),
                            category="education_certifications",
                            importance="medium",
                            required_or_preferred="required",
                            weight=1.0,
                            aliases=[degree_name.lower(), field.lower()],
                        )
                    )

        # 3. Known Skills Catalog
        for skill_name, info in KNOWN_SKILLS_CATALOG.items():
            pattern = r"\b" + re.escape(skill_name) + r"\b"
            matched = False
            if re.search(pattern, jd_lower):
                matched = True
            else:
                for alias in info["aliases"]:
                    if re.search(r"\b" + re.escape(alias) + r"\b", jd_lower):
                        matched = True
                        break

            if matched:
                req_key = f"skill_{skill_name}"
                if req_key not in seen_keys:
                    seen_keys.add(req_key)
                    req_id = f"req_{len(requirements) + 1}_{uuid4().hex[:6]}"
                    cat = info["category"]
                    importance = "high" if cat in ("programming_languages", "databases", "apis_backend", "frameworks_libraries") else "medium"
                    weight = 1.2 if importance == "high" else 0.8
                    requirements.append(
                        JDRequirement(
                            requirement_id=req_id,
                            text=skill_name.title() if len(skill_name) > 3 else skill_name.upper(),
                            normalized_name=skill_name,
                            category=cat,
                            importance=importance,
                            required_or_preferred="required",
                            weight=weight,
                            aliases=info["aliases"],
                        )
                    )

        # 4. Fallback check with KeywordService for any additional tech skills
        existing_keywords = KeywordService.extract(job_description)
        for kw in existing_keywords:
            req_key = f"skill_{kw}"
            if req_key not in seen_keys:
                seen_keys.add(req_key)
                req_id = f"req_{len(requirements) + 1}_{uuid4().hex[:6]}"
                requirements.append(
                    JDRequirement(
                        requirement_id=req_id,
                        text=kw.title(),
                        normalized_name=kw,
                        category="other",
                        importance="medium",
                        required_or_preferred="required",
                        weight=1.0,
                        aliases=[],
                    )
                )

        return requirements

    @classmethod
    def extract_with_llm(cls, job_description: str) -> list[JDRequirement] | None:
        """
        Uses LLM to extract structured requirements.
        Returns None if extraction fails so deterministic fallback is used.
        """
        prompt = f"""
You are an expert technical recruiter analyzing a job description.
Extract all key requirements (technical skills, experience years, education, frameworks, databases, cloud, soft skills).
Preserve the exact requirement and DO NOT hallucinate.

Job Description:
\"\"\"
{job_description[:3000]}
\"\"\"

Return ONLY a JSON array of objects with the following keys:
- "text": string (e.g. "3+ years Python experience", "FastAPI", "PostgreSQL", "Bachelor's degree in Computer Science")
- "normalized_name": string (standardized lowercase name, e.g. "python", "fastapi")
- "category": one of ["programming_languages", "frameworks_libraries", "databases", "apis_backend", "cloud_devops", "data_structures_algorithms", "education_certifications", "professional_experience", "soft_skills", "other"]
- "importance": "critical", "high", "medium", or "low"
- "required_or_preferred": "required" or "preferred"
- "weight": float (between 0.5 and 2.0)
- "aliases": list of strings (alternative terms, e.g. ["py", "python3"])
- "years_required": float or null (number of years if specified)

JSON:
"""
        try:
            raw_response = llm_service.generate(prompt).strip()
            # Clean markdown wrappers if present
            if raw_response.startswith("```json"):
                raw_response = raw_response[7:]
            if raw_response.startswith("```"):
                raw_response = raw_response[3:]
            if raw_response.endswith("```"):
                raw_response = raw_response[:-3]
            raw_response = raw_response.strip()

            parsed = json.loads(raw_response)
            if not isinstance(parsed, list):
                return None

            requirements: list[JDRequirement] = []
            for i, item in enumerate(parsed):
                if not isinstance(item, dict) or not item.get("text"):
                    continue
                req_id = f"req_{i+1}_{uuid4().hex[:6]}"
                requirements.append(
                    JDRequirement(
                        requirement_id=req_id,
                        text=str(item["text"]).strip(),
                        normalized_name=str(item.get("normalized_name") or item["text"]).strip().lower(),
                        category=str(item.get("category") or "other"),
                        importance=str(item.get("importance") or "medium"),
                        required_or_preferred=str(item.get("required_or_preferred") or "required"),
                        weight=float(item.get("weight") or 1.0),
                        aliases=[str(a).strip().lower() for a in item.get("aliases", []) if str(a).strip()],
                        years_required=float(item["years_required"]) if item.get("years_required") is not None else None,
                    )
                )

            return requirements if requirements else None
        except Exception as exc:
            logger.warning("LLM requirement extraction failed, falling back to deterministic extraction: %s", exc)
            return None

    @classmethod
    def extract_requirements(cls, job_description: str, use_llm: bool = False) -> list[JDRequirement]:
        """
        Main extraction entry point.
        By default or on LLM error, uses deterministic extraction to guarantee fast, reliable, reproducible extraction.
        """
        if not job_description or not job_description.strip():
            return []

        if use_llm:
            llm_reqs = cls.extract_with_llm(job_description)
            if llm_reqs:
                return llm_reqs

        # Guaranteed deterministic extraction
        return cls.extract_deterministic(job_description)


requirement_extractor = RequirementExtractor()
