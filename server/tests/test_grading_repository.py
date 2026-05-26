"""
tests/test_grading_repository.py — בדיקות יחידה ל-Repository
משתמש ב-SQLite in-memory במקום SQL Server
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.models.models import Base, GradingResult, ConceptEvaluation
from server.dtos.dtos import ConceptEvaluationDTO
from server.repositories.grading_repository import GradingRepository
from server.exceptions.exceptions import DatabaseError


@pytest.fixture
def db_session():
    """SQLite in-memory — מהיר, ללא SQL Server."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def repo(db_session):
    return GradingRepository(db_session)


SAMPLE_BREAKDOWN = [
    ConceptEvaluationDTO(
        concept="פולימורפיזם",
        similarity=0.85,
        best_segment="פולימורפיזם מאפשר גמישות",
        negation_detected=False,
        status="correct",
    ),
    ConceptEvaluationDTO(
        concept="ירושה",
        similarity=0.45,
        best_segment="לא נעשה שימוש בירושה",
        negation_detected=True,
        status="negated",
    ),
]


# ══════════════════════════════════════════════════════════════
class TestSaveResult:

    def test_save_creates_grading_result(self, repo, db_session):
        result = repo.save_result(
            submission_id=1,
            final_score=0.75,
            confidence="low",
            needs_llm_review=True,
            needs_human_review=True,
            breakdown=SAMPLE_BREAKDOWN,
        )
        assert result.id is not None
        assert result.submission_id == 1
        assert result.final_score == 0.75

    def test_save_creates_concept_evaluations(self, repo, db_session):
        result = repo.save_result(
            submission_id=2,
            final_score=0.5,
            confidence="low",
            needs_llm_review=True,
            needs_human_review=False,
            breakdown=SAMPLE_BREAKDOWN,
        )
        concepts = (
            db_session.query(ConceptEvaluation)
            .filter_by(grading_result_id=result.id)
            .all()
        )
        assert len(concepts) == 2
        assert concepts[0].concept == "פולימורפיזם"
        assert concepts[1].status == "negated"

    def test_save_with_empty_breakdown(self, repo, db_session):
        result = repo.save_result(
            submission_id=3,
            final_score=1.0,
            confidence="high",
            needs_llm_review=False,
            needs_human_review=False,
            breakdown=[],
        )
        assert result.id is not None
        concepts = (
            db_session.query(ConceptEvaluation)
            .filter_by(grading_result_id=result.id)
            .all()
        )
        assert len(concepts) == 0


# ══════════════════════════════════════════════════════════════
class TestGetById:

    def test_get_existing_result(self, repo):
        saved = repo.save_result(1, 0.8, "high", False, False, SAMPLE_BREAKDOWN)
        fetched = repo.get_by_id(saved.id)
        assert fetched is not None
        assert fetched.id == saved.id

    def test_get_nonexistent_returns_none(self, repo):
        result = repo.get_by_id(9999)
        assert result is None


# ══════════════════════════════════════════════════════════════
class TestGetBySubmission:

    def test_returns_all_results_for_submission(self, repo):
        repo.save_result(5, 0.6, "low", True, False, SAMPLE_BREAKDOWN)
        repo.save_result(5, 0.9, "high", False, False, SAMPLE_BREAKDOWN)
        results = repo.get_by_submission(5)
        assert len(results) == 2

    def test_returns_empty_for_unknown_submission(self, repo):
        results = repo.get_by_submission(9999)
        assert results == []


# ══════════════════════════════════════════════════════════════
class TestGetPendingHumanReview:

    def test_returns_only_flagged(self, repo):
        repo.save_result(10, 0.5, "low", True,  True,  SAMPLE_BREAKDOWN)
        repo.save_result(11, 0.9, "high", False, False, SAMPLE_BREAKDOWN)
        pending = repo.get_pending_human_review()
        assert len(pending) == 1
        assert pending[0].submission_id == 10
