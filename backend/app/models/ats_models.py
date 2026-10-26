from typing import Any
from pydantic import BaseModel, Field


class ATSRequest(BaseModel):
    session_id: str = Field(
        ...,
        description="Session ID returned after resume upload."
    )
    job_description: str = Field(
        ...,
        min_length=20,
    )


class JDRequirement(BaseModel):
    requirement_id: str
    text: str
    normalized_name: str | None = None
    category: str = "other"
    importance: str = "medium"  # critical, high, medium, low
    required_or_preferred: str = "required"  # required, preferred
    weight: float = 1.0
    aliases: list[str] = Field(default_factory=list)
    years_required: float | None = None


class RequirementEvidence(BaseModel):
    requirement_id: str
    requirement_text: str
    category: str = "other"
    importance: str = "medium"
    required_or_preferred: str = "required"
    weight: float = 1.0
    matching_keywords: list[str] = Field(default_factory=list)
    retrieved_passages: list[str] = Field(default_factory=list)
    source_chunk_ids: list[str] = Field(default_factory=list)
    similarity_score: float | None = None
    has_keyword_match: bool = False
    has_semantic_match: bool = False
    status: str = "no_evidence_found"  # matched, partial_match, no_evidence_found, uncertain
    confidence: float = 0.0
    score: float = 0.0  # 1.0 for matched, 0.5 for partial_match, 0.0 for no_evidence_found / uncertain
    reasoning: str = ""


class ATSScoreBreakdown(BaseModel):
    by_category: dict[str, dict[str, Any]] = Field(default_factory=dict)
    total_requirements: int = 0
    matched_count: int = 0
    partial_count: int = 0
    missing_count: int = 0
    uncertain_count: int = 0
    total_evaluated_weight: float = 0.0
    total_weight: float = 0.0


class ATSAnalysisResponseData(BaseModel):
    # Backward compatible fields
    ats_score: int
    semantic_similarity: float
    matching_skills: list[str]
    missing_skills: list[str]
    ai_feedback: dict[str, Any]

    # Enhanced requirement-level fields
    weighted_coverage_score: float
    evaluation_coverage: float
    keyword_coverage: float
    semantic_evidence_coverage: float
    partial_matches: list[str] = Field(default_factory=list)
    uncertain_requirements: list[str] = Field(default_factory=list)
    evidence_summary: dict[str, int] = Field(default_factory=dict)
    score_breakdown: dict[str, Any] = Field(default_factory=dict)
    requirement_results: list[dict[str, Any]] = Field(default_factory=list)
    analysis_status: str = "completed"