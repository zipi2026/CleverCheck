"""
dtos/dtos.py — Data Transfer Objects בין שכבות
"""
from dataclasses import dataclass, asdict, field


# ── קלט ──────────────────────────────────────────────────────
@dataclass
class GradeRequestDTO:
    """קלט מה-Controller לשירות."""
    submission_id: int
    student_answer: str
    key_concepts: list[str]


# ── פלט ביניים ───────────────────────────────────────────────
@dataclass
class ConceptEvaluationDTO:
    """פירוט מושג בודד — עובר בין Service ל-Repository ול-Controller."""
    concept: str
    similarity: float
    best_segment: str
    negation_detected: bool
    status: str  # "correct" | "negated" | "missing"

    def to_dict(self) -> dict:
        return asdict(self)


# ── פלט סופי ─────────────────────────────────────────────────
@dataclass
class GradeResponseDTO:
    """פלט מלא שחוזר מה-Service ל-Controller."""
    grading_result_id: int
    submission_id: int
    score: float                          # 0–100
    confidence: str                       # "high" / "low"
    needs_llm_review: bool
    needs_human_review: bool
    breakdown: list[ConceptEvaluationDTO] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "grading_result_id": self.grading_result_id,
            "submission_id":     self.submission_id,
            "score":             self.score,
            "confidence":        self.confidence,
            "needs_llm_review":  self.needs_llm_review,
            "needs_human_review": self.needs_human_review,
            "breakdown":         [b.to_dict() for b in self.breakdown],
        }
