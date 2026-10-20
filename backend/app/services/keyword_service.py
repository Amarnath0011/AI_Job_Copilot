import re


# Canonical skill -> common ways the skill appears in resumes and JDs.
# Matches are returned using the canonical name so aliases compare correctly.
SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "java": ("java",),
    "python": ("python",),
    "c": ("c language", "programming in c", "language c"),
    "c++": ("c++", "cpp", "cplusplus"),
    "c#": ("c#", "c sharp"),
    "javascript": ("javascript", "js", "ecmascript"),
    "typescript": ("typescript", "ts"),
    "go": ("golang",),
    "rust": ("rust",),
    "kotlin": ("kotlin",),
    "php": ("php",),
    "oop": ("oop", "object oriented programming", "object-oriented programming"),
    "data structures": ("data structures", "data structure"),
    "algorithms": ("algorithms", "algorithm"),
    "problem solving": ("problem solving", "problem-solving"),
    "operating systems": ("operating systems", "operating system", "os concepts"),
    "computer networks": ("computer networks", "computer networking", "networking fundamentals"),
    "dbms": ("dbms", "database management systems"),
    "sql": ("sql",),
    "html": ("html", "html5"),
    "css": ("css", "css3"),
    "react": ("react", "react.js", "reactjs"),
    "redux": ("redux",),
    "next.js": ("next.js", "nextjs"),
    "tailwind css": ("tailwind css", "tailwind"),
    "bootstrap": ("bootstrap",),
    "node.js": ("node", "node.js", "nodejs"),
    "express.js": ("express", "express.js", "expressjs"),
    "fastapi": ("fastapi", "fast api"),
    "flask": ("flask",),
    "django": ("django",),
    "spring": ("spring framework",),
    "spring boot": ("spring boot", "springboot"),
    "hibernate": ("hibernate",),
    "mysql": ("mysql",),
    "postgresql": ("postgresql", "postgres"),
    "mongodb": ("mongodb", "mongo db"),
    "redis": ("redis",),
    "sqlite": ("sqlite", "sqlite3"),
    "docker": ("docker",),
    "kubernetes": ("kubernetes", "k8s"),
    "aws": ("aws", "amazon web services"),
    "azure": ("azure", "microsoft azure"),
    "gcp": ("gcp", "google cloud platform"),
    "jenkins": ("jenkins",),
    "terraform": ("terraform",),
    "github actions": ("github actions",),
    "git": ("git",),
    "github": ("github",),
    "linux": ("linux",),
    "bash": ("bash",),
    "command line": ("command line", "command-line", "cli"),
    "rest api": ("rest api", "rest apis", "restful api", "restful apis", "restful services"),
    "graphql": ("graphql", "graph ql"),
    "microservices": ("microservices", "micro-services"),
    "ai": ("artificial intelligence", "ai"),
    "machine learning": ("machine learning", "ml"),
    "deep learning": ("deep learning",),
    "llm": ("llm", "llms", "large language model", "large language models"),
    "rag": ("rag", "retrieval augmented generation", "retrieval-augmented generation"),
    "langchain": ("langchain",),
    "llamaindex": ("llamaindex", "llama index", "llama-index"),
    "chromadb": ("chromadb", "chroma db", "chroma"),
    "faiss": ("faiss",),
    "pinecone": ("pinecone",),
    "hugging face": ("hugging face", "huggingface"),
    "openai": ("openai",),
    "groq": ("groq",),
    "gemini": ("gemini", "google gemini"),
    "prompt engineering": ("prompt engineering",),
    "ai agents": ("ai agents", "agentic ai"),
    "embeddings": ("embeddings", "embedding models"),
    "tensorflow": ("tensorflow",),
    "pytorch": ("pytorch", "torch"),
    "numpy": ("numpy",),
    "pandas": ("pandas",),
    "scikit-learn": ("scikit-learn", "scikit learn", "sklearn"),
    "software engineering": ("software engineering",),
    "design patterns": ("design patterns",),
    "unit testing": ("unit testing", "unit tests"),
    "system design": ("system design",),
}


def _phrase_pattern(phrase: str) -> re.Pattern[str]:
    """Match a phrase without requiring a word boundary after punctuation (C++/C#)."""
    escaped = re.escape(phrase.lower()).replace(r"\ ", r"\s+")
    # ASCII alphanumeric boundaries allow punctuation-heavy names like C++ and C#.
    return re.compile(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])", re.IGNORECASE)


class KeywordService:
    # Backwards-compatible set for callers that inspect the supported skills.
    TECH_SKILLS = set(SKILL_ALIASES)

    _PATTERNS = {
        canonical: tuple(_phrase_pattern(alias) for alias in aliases)
        for canonical, aliases in SKILL_ALIASES.items()
    }

    @classmethod
    def extract(cls, text: str) -> set[str]:
        if not text:
            return set()

        found_skills: set[str] = set()
        for canonical, patterns in cls._PATTERNS.items():
            if any(pattern.search(text) for pattern in patterns):
                found_skills.add(canonical)

        return found_skills
