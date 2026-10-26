import json
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from langchain_core.documents import Document
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_current_user
from app.ats.evaluator import EvidenceEvaluator
from app.ats.evidence_retriever import EvidenceRetriever
from app.ats.requirement_extractor import RequirementExtractor
from app.ats.scorer import ATSScorer
from app.db.base import Base
from app.db.database import get_db
from app.db.models import Resume, User
from app.main import app
from app.models.ats_models import JDRequirement, RequirementEvidence
from app.services.ats_service import ats_service
from app.services.similarity_service import SimilarityService


# Mock vector store helper for testing
class MockVectorStore:
    def __init__(self, docs_by_session: dict[str, list[Document]] | None = None):
        self.docs_by_session = docs_by_session or {}

    def similarity_search(self, query: str, k: int = 2, filter: dict | None = None) -> list[Document]:
        session_id = None
        if filter and "$and" in filter:
            for condition in filter["$and"]:
                if "session_id" in condition:
                    session_id = condition["session_id"]
        elif filter and "session_id" in filter:
            session_id = filter["session_id"]

        available_docs = self.docs_by_session.get(session_id, [])
        # Return docs that contain any token from query or return top k
        matching = [d for d in available_docs if any(w.lower() in d.page_content.lower() for w in query.split())]
        return matching[:k] if matching else available_docs[:k]

    def similarity_search_with_relevance_scores(self, query: str, k: int = 2, filter: dict | None = None):
        docs = self.similarity_search(query, k=k, filter=filter)
        return [(doc, 0.85) for doc in docs]


# ==============================================================================
# A. Complete-Resume Coverage Test
# ==============================================================================
def test_complete_resume_coverage_discovers_skills_in_later_chunks():
    """
    Test A: Create a resume where early text has Python & FastAPI,
    and later sections have SQL, Docker, AWS.
    Verify that ALL skills are discovered through complete-resume evaluation.
    """
    resume_text = (
        "SUMMARY\n"
        "Backend developer with expertise in Python and FastAPI.\n\n"
        "EXPERIENCE\n"
        "Senior Software Engineer at TechCorp (3 years).\n"
        "Developed microservices using Python and FastAPI framework.\n\n"
        "PROJECTS\n"
        "Cloud Migration Project: Containerized backend services with Docker and deployed to AWS.\n"
        "Managed relational database schemas using PostgreSQL and optimized SQL queries.\n"
    )

    jd = (
        "We are looking for a Backend Engineer with experience in Python, FastAPI, "
        "SQL, Docker, and AWS."
    )

    # Simulate vector store that only has chunk covering Python & FastAPI
    top_chunk_only_store = MockVectorStore({
        "session-123": [
            Document(page_content="Backend developer with expertise in Python and FastAPI.", metadata={"session_id": "session-123", "document_type": "resume"})
        ]
    })

    result = ats_service.analyze(
        resume_text=resume_text,
        job_description=jd,
        session_id="session-123",
        vector_store=top_chunk_only_store,
    )

    # Even though vector store chunk only had Python and FastAPI,
    # full resume analysis must discover SQL, Docker, and AWS!
    matching = [s.lower() for s in result["matching_skills"]]
    assert "python" in matching
    assert "fastapi" in matching
    assert any("sql" in s for s in matching)
    assert any("docker" in s for s in matching)
    assert any("aws" in s for s in matching)
    assert result["ats_score"] >= 80


# ==============================================================================
# B. Missing Evidence / No False Positives Test
# ==============================================================================
def test_jd_requirements_with_no_supporting_evidence():
    """
    Test B: Include skills in JD not present anywhere in the resume.
    Verify they are reported as missing and not matched.
    """
    resume_text = "Junior developer with 1 year experience in JavaScript, HTML, and CSS."
    jd = "Required: Rust programming language, Kubernetes cluster administration, and GraphQL APIs."

    result = ats_service.analyze(
        resume_text=resume_text,
        job_description=jd,
        session_id="session-empty",
        vector_store=MockVectorStore(),
    )

    missing = [s.lower() for s in result["missing_skills"]]
    matching = [s.lower() for s in result["matching_skills"]]

    assert any("rust" in m for m in missing)
    assert any("kubernetes" in m for m in missing)
    assert any("graphql" in m for m in missing)

    # Must NOT have false matches
    assert not any("rust" in m for m in matching)
    assert not any("kubernetes" in m for m in matching)
    assert result["ats_score"] == 0
    assert result["evidence_summary"]["no_evidence_found"] >= 3


# ==============================================================================
# C. Semantic Match With Different Phrasing Test
# ==============================================================================
def test_semantic_match_with_different_wording():
    """
    Test C: JD requires RESTful APIs; resume says 'Implemented HTTP endpoints using FastAPI'.
    Verify contextual matching without hallucinating direct quotes.
    """
    resume_text = (
        "Software Engineer with 2 years experience. "
        "Implemented high-performance HTTP endpoints using FastAPI for mobile clients."
    )
    jd = "Requirements: Experience with RESTful APIs and backend services."

    mock_store = MockVectorStore({
        "session-sem": [
            Document(
                page_content="Implemented high-performance HTTP endpoints using FastAPI for mobile clients.",
                metadata={"session_id": "session-sem", "document_type": "resume"}
            )
        ]
    })

    result = ats_service.analyze(
        resume_text=resume_text,
        job_description=jd,
        session_id="session-sem",
        vector_store=mock_store,
    )

    # Matching or partial match found through semantic/contextual reasoning
    all_matched = [s.lower() for s in result["matching_skills"] + result["partial_matches"]]
    assert any("rest" in s or "api" in s for s in all_matched)

    # Verify requirement results have evidence passage
    req_res = result["requirement_results"]
    api_req = next((r for r in req_res if "rest" in r["requirement_text"].lower() or "api" in r["requirement_text"].lower()), None)
    assert api_req is not None
    assert api_req["status"] in ("matched", "partial_match")
    assert len(api_req["retrieved_passages"]) > 0


# ==============================================================================
# D. Experience Duration Mismatch Test
# ==============================================================================
def test_experience_duration_mismatch():
    """
    Test D: JD requires 3 years professional Python experience.
    Resume mentions Python in a college/university student project.
    Verify keyword presence does not falsely verify 3 years professional experience.
    """
    requirement = JDRequirement(
        requirement_id="req-py-3yrs",
        text="3+ years of professional experience in Python",
        normalized_name="python",
        category="professional_experience",
        importance="critical",
        weight=1.5,
        years_required=3.0,
    )

    # Academic only evidence
    evidence = RequirementEvidence(
        requirement_id=requirement.requirement_id,
        requirement_text=requirement.text,
        category=requirement.category,
        weight=requirement.weight,
        matching_keywords=["python"],
        retrieved_passages=["Developed a Python project during college as an undergraduate student."],
        has_keyword_match=True,
        has_semantic_match=True,
    )

    evaluated = EvidenceEvaluator.evaluate_requirement_deterministic(requirement, evidence)

    # Must be partial_match, NOT matched!
    assert evaluated.status == "partial_match"
    assert evaluated.score == 0.5
    assert "academic" in evaluated.reasoning.lower() or "project" in evaluated.reasoning.lower()


# ==============================================================================
# E. Session Isolation Test
# ==============================================================================
def test_session_isolation_never_mixes_sessions():
    """
    Test E: Session A has Java & Spring Boot.
    Session B has Python & FastAPI.
    Analysis for Session A must never retrieve Session B chunks.
    """
    mock_store = MockVectorStore({
        "session-A": [
            Document(page_content="Expert in Java, Spring Boot, and MySQL.", metadata={"session_id": "session-A", "document_type": "resume"})
        ],
        "session-B": [
            Document(page_content="Expert in Python, FastAPI, and MongoDB.", metadata={"session_id": "session-B", "document_type": "resume"})
        ],
    })

    # Lexical evidence retriever semantic call for session A
    req_python = JDRequirement(requirement_id="req-py", text="Python", normalized_name="python")
    evidence_A = EvidenceRetriever.collect_evidence_for_requirement(
        requirement=req_python,
        full_resume_text="Java and Spring Boot developer.",
        session_id="session-A",
        vector_store=mock_store,
    )

    # Session A does not have Python in text or in session-A vector store!
    assert not evidence_A.has_keyword_match
    # Chunks from session-B must NOT be retrieved
    for p in evidence_A.retrieved_passages:
        assert "FastAPI" not in p
        assert "MongoDB" not in p


from sqlalchemy.pool import StaticPool

# ==============================================================================
# F. Empty or Invalid Session Test
# ==============================================================================
def test_unknown_session_returns_404():
    """
    Test F: Requesting analysis for an unknown session returns 404.
    """
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine, expire_on_commit=False)

    user = User(id=1, name="Test User", email="test@example.com", password_hash="hash")
    with TestSession() as db:
        db.add(user)
        db.commit()

    def override_get_db():
        with TestSession() as session:
            yield session

    def override_get_current_user():
        return user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    response = client.post(
        "/ats/analyze",
        json={"session_id": str(uuid4()), "job_description": "We need a Python and SQL backend engineer."},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()



# ==============================================================================
# G. No Requirements Extracted / Division by Zero Test
# ==============================================================================
def test_no_requirements_extracted_does_not_divide_by_zero():
    """
    Test G: A job description that yields no recognizable requirements
    should not crash or return a fake 100%.
    """
    jd_empty_or_vague = "Our team values high collaboration, curiosity, and good communication in a friendly workplace."

    # Force extractor to return empty list
    with patch.object(RequirementExtractor, "extract_requirements", return_value=[]):
        result = ATSScorer.score(
            resume_text="Software engineer with strong experience.",
            job_description=jd_empty_or_vague,
        )

    assert result["ats_score"] == 0
    assert result["weighted_coverage_score"] == 0.0
    assert result["analysis_status"] == "no_requirements_found"
    assert result["matching_skills"] == []
    assert result["missing_skills"] == []


# ==============================================================================
# H. LLM or Retrieval Failure Resilience Test
# ==============================================================================
def test_llm_and_retrieval_failure_fallback():
    """
    Test H: Simulate LLM timeout/invalid JSON and retrieval error.
    System must handle gracefully without converting error to match or crashing.
    """
    resume_text = "Proficient in Python, SQL, and Git."
    jd = "Looking for Python, SQL, and Docker developer."

    # Simulate LLM throwing an exception
    with patch("app.services.llm_service.llm_service.generate", side_effect=RuntimeError("Groq API Timeout")):
        result = ats_service.analyze(
            resume_text=resume_text,
            job_description=jd,
            session_id="session-resilient",
            vector_store=None,  # No vector store -> lexical fallback
        )

    assert result["ats_score"] > 0
    assert "Python" in result["matching_skills"] or "python" in [s.lower() for s in result["matching_skills"]]
    # Feedback fallback generated successfully despite LLM failure
    assert "ai_feedback" in result
    assert "overall_feedback" in result["ai_feedback"]
    assert len(result["ai_feedback"]["strengths"]) > 0


# ==============================================================================
# I. Long Resume / Embedding Limits Test
# ==============================================================================
def test_long_resume_handles_token_limits_safely():
    """
    Test I: Resume exceeding single embedding token limit (~10,000 chars).
    Verify similarity calculation works without error and deterministic checks succeed.
    """
    # Create ~12,000 characters synthetic resume
    long_resume = (
        "John Doe - Senior Architect\n"
        + ("Experienced in high-throughput distributed systems and enterprise architecture.\n" * 150)
        + "\nTECHNICAL SKILLS\n"
        + "Java, Spring Boot, Python, FastAPI, Docker, Kubernetes, AWS, PostgreSQL, Redis\n"
    )

    jd = "Required: Python, FastAPI, Docker, and PostgreSQL."

    # Chunk-aware similarity calculation must succeed without error
    sim = SimilarityService.calculate_similarity(long_resume, jd)
    assert 0.0 <= sim <= 1.0

    # Scorer should still find the skills placed at the very end of the 12,000-char document!
    result = ATSScorer.score(long_resume, jd)
    matching = [s.lower() for s in result["matching_skills"]]
    assert "python" in matching
    assert "fastapi" in matching
    assert "docker" in matching
    assert "postgresql" in matching
    assert result["ats_score"] >= 90


# ==============================================================================
# J. Duplicate Chunks Deduplication Test
# ==============================================================================
def test_duplicate_chunks_do_not_inflate_score():
    """
    Test J: Duplicate or overlapping chunks from vector store must be deduplicated
    and not count duplicate evidence multiple times.
    """
    req = JDRequirement(requirement_id="req-1", text="Docker", normalized_name="docker")
    # Feed identical chunk 4 times
    dup_store = MockVectorStore({
        "session-dup": [
            Document(page_content="Containerized services using Docker.", metadata={"session_id": "session-dup", "document_type": "resume"}),
            Document(page_content="Containerized services using Docker.", metadata={"session_id": "session-dup", "document_type": "resume"}),
            Document(page_content="Containerized services using Docker.", metadata={"session_id": "session-dup", "document_type": "resume"}),
        ]
    })

    evidence = EvidenceRetriever.collect_evidence_for_requirement(
        requirement=req,
        full_resume_text="Containerized services using Docker.",
        session_id="session-dup",
        vector_store=dup_store,
    )

    # Passages must be deduplicated
    assert len(evidence.retrieved_passages) == 1


# ==============================================================================
# K. Backward Compatibility & API Regression Test
# ==============================================================================
def test_api_regression_and_backward_compatibility():
    """
    Test K: Verify that /ats/analyze request and response structure retain
    all legacy fields and expected schema.
    """
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine, expire_on_commit=False)


    user = User(id=1, name="Test User", email="test@example.com", password_hash="hash")
    session_id = str(uuid4())
    resume = Resume(
        id=str(uuid4()),
        session_id=session_id,
        user_id=user.id,
        original_filename="sample.pdf",
        cloudinary_url="https://example.com/res.pdf",
        cloudinary_public_id="res123",
        extracted_text="Experienced Python and FastAPI developer with SQL experience.",
    )

    with TestSession() as db:
        db.add_all([user, resume])
        db.commit()

    def override_get_db():
        with TestSession() as session:
            yield session

    def override_get_current_user():
        return user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    response = client.post(
        "/ats/analyze",
        json={
            "session_id": session_id,
            "job_description": "We are seeking a Python and SQL backend engineer to join our team.",
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "data" in body

    data = body["data"]

    # Verify all legacy fields exist
    assert "ats_score" in data
    assert isinstance(data["ats_score"], int)
    assert "semantic_similarity" in data
    assert "matching_skills" in data
    assert isinstance(data["matching_skills"], list)
    assert "missing_skills" in data
    assert isinstance(data["missing_skills"], list)
    assert "ai_feedback" in data

    # Verify AI feedback contract fields
    fb = data["ai_feedback"]
    assert "overall_feedback" in fb
    assert "strengths" in fb
    assert "weaknesses" in fb
    assert "resume_summary" in fb
    assert "improved_summary" in fb
    assert "recommended_keywords" in fb
    assert "improvement_suggestions" in fb

    # Verify new enhanced fields exist
    assert "weighted_coverage_score" in data
    assert "score_breakdown" in data
    assert "requirement_results" in data
    assert "evaluation_coverage" in data
    assert "keyword_coverage" in data
    assert "evidence_summary" in data
    assert "analysis_status" in data
