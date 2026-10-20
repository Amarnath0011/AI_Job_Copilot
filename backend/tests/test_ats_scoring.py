from app.ats.scorer import ATSScorer
from app.services.keyword_service import KeywordService
from app.services.similarity_service import SimilarityService


def test_keyword_aliases_normalize_to_canonical_skills():
    text = "Built APIs with JS, ReactJS, NodeJS, Postgres, sklearn, and RESTful services."
    skills = KeywordService.extract(text)

    assert {"javascript", "react", "node.js", "postgresql", "scikit-learn", "rest api"} <= skills


def test_punctuation_heavy_languages_are_detected():
    skills = KeywordService.extract("Proficient in C++, C#, and Python.")

    assert "c++" in skills
    assert "c#" in skills
    assert "python" in skills
    assert "c" not in skills


def test_empty_text_returns_no_skills():
    assert KeywordService.extract("") == set()


def test_scorer_returns_explainable_breakdown(monkeypatch):
    monkeypatch.setattr(
        SimilarityService,
        "calculate_similarity",
        staticmethod(lambda resume_text, job_description: 0.95),
    )

    result = ATSScorer.score(
        resume_text="Python FastAPI MySQL Docker",
        job_description="Python FastAPI MySQL Docker",
    )

    assert result["ats_score"] == 98
    assert result["keyword_score"] == 100.0
    assert result["semantic_score"] == 95.0
    assert result["matching_skills"] == ["docker", "fastapi", "mysql", "python"]
    assert result["missing_skills"] == []


def test_missing_required_skill_reduces_keyword_coverage(monkeypatch):
    monkeypatch.setattr(
        SimilarityService,
        "calculate_similarity",
        staticmethod(lambda resume_text, job_description: 0.80),
    )

    result = ATSScorer.score(
        resume_text="Python FastAPI MySQL",
        job_description="Python FastAPI MySQL Docker",
    )

    assert result["keyword_score"] == 75.0
    assert result["missing_skills"] == ["docker"]
    assert result["ats_score"] == 77


def test_similarity_chunking_covers_long_text_and_handles_empty_text():
    text = ("Python and FastAPI build reliable services. " * 100)
    chunks = SimilarityService._split_text(text)

    assert len(chunks) > 1
    assert all(0 < len(chunk) <= SimilarityService.CHUNK_SIZE for chunk in chunks)
    assert SimilarityService._split_text("") == []
