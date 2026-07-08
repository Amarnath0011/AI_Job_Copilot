import re


class KeywordService:

    TECH_SKILLS = {
        "java",
        "python",
        "c++",
        "javascript",
        "typescript",
        "react",
        "node",
        "express",
        "spring",
        "spring boot",
        "hibernate",
        "fastapi",
        "django",
        "flask",
        "mysql",
        "postgresql",
        "mongodb",
        "redis",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "git",
        "github",
        "rest",
        "rest api",
        "microservices",
        "langchain",
        "chroma",
        "chromadb",
        "hugging face",
        "huggingface",
        "llm",
        "rag",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas"
    }

    @classmethod
    def extract(cls, text: str) -> set[str]:

        text = text.lower()

        skills = set()

        for skill in cls.TECH_SKILLS:
            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text):
                skills.add(skill)

        return skills