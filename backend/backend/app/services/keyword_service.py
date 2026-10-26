import re


class KeywordService:

    TECH_SKILLS = {

        # ==========================
        # Programming Languages
        # ==========================
        "java",
        "python",
        "c",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "go",
        "rust",
        "kotlin",
        "php",

        # ==========================
        # CS Fundamentals
        # ==========================
        "oop",
        "object oriented programming",
        "data structures",
        "algorithms",
        "problem solving",
        "operating systems",
        "computer networks",
        "dbms",
        "sql",

        # ==========================
        # Frontend
        # ==========================
        "html",
        "css",
        "react",
        "redux",
        "next.js",
        "tailwind css",
        "bootstrap",

        # ==========================
        # Backend
        # ==========================
        "node",
        "express",
        "fastapi",
        "flask",
        "django",
        "spring",
        "spring boot",
        "hibernate",

        # ==========================
        # Databases
        # ==========================
        "mysql",
        "postgresql",
        "mongodb",
        "redis",
        "sqlite",

        # ==========================
        # Cloud & DevOps
        # ==========================
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "jenkins",
        "terraform",
        "github actions",

        # ==========================
        # Version Control & Tools
        # ==========================
        "git",
        "github",
        "linux",
        "bash",
        "command line",
        "command-line",

        # ==========================
        # APIs & Architecture
        # ==========================
        "rest",
        "rest api",
        "graphql",
        "microservices",

        # ==========================
        # AI / GenAI
        # ==========================
        "ai",
        "machine learning",
        "deep learning",
        "llm",
        "rag",
        "langchain",
        "llamaindex",
        "chromadb",
        "faiss",
        "pinecone",
        "hugging face",
        "openai",
        "groq",
        "gemini",
        "prompt engineering",
        "ai agents",
        "embeddings",

        # ==========================
        # AI Libraries
        # ==========================
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas",
        "scikit-learn",

        # ==========================
        # Software Engineering
        # ==========================
        "software engineering",
        "software engineering best practices",
        "design patterns",
        "unit testing",
        "system design",
    }

    @classmethod
    def extract(cls, text: str) -> set[str]:

        text = text.lower()

        found_skills = set()

        for skill in cls.TECH_SKILLS:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, text):
                found_skills.add(skill.lower())

        return found_skills