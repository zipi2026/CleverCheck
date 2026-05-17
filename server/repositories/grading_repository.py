"""
repositories/grading_repository.py — גישה למסד הנתונים
"""
import logging
from sqlalchemy.orm import Session
from models.models import GradingResult, ConceptEvaluation
from dtos.dtos import ConceptEvaluationDTO, GradeResponseDTO
from exceptions.exceptions import DatabaseError

logger = logging.getLogger(__name__)


class GradingRepository:
    def __init__(self, db: Session):
        self._db = db

    # ── כתיבה ─────────────────────────────────────────────────
    def save_result(
        self,
        submission_id: int,
        final_score: float,
        confidence: str,
        needs_llm_review: bool,
        needs_human_review: bool,
        breakdown: list[ConceptEvaluationDTO],
    ) -> GradingResult:
        """
        שומר GradingResult + רשימת ConceptEvaluation בטרנזקציה אחת.
        משתמש ב-bulk_save_objects לביצועים.
        """
        try:
            result = GradingResult(
                submission_id=submission_id,
                final_score=final_score,
                confidence=confidence,
                needs_llm_review=needs_llm_review,
                needs_human_review=needs_human_review,
            )
            self._db.add(result)
            self._db.flush()  # מקבל ID לפני commit

            evaluations = [
                ConceptEvaluation(
                    grading_result_id=result.id,
                    concept=dto.concept,
                    similarity=dto.similarity,
                    best_segment=dto.best_segment,
                    negation_detected=dto.negation_detected,
                    status=dto.status,
                )
                for dto in breakdown
            ]
            self._db.bulk_save_objects(evaluations)
            self._db.commit()

            logger.info(f"Saved GradingResult id={result.id} submission={submission_id}")
            return result

        except Exception as exc:
            self._db.rollback()
            logger.error(f"DB save failed: {exc}")
            raise DatabaseError(f"שמירת תוצאה נכשלה: {exc}")

    # ── קריאה ─────────────────────────────────────────────────
    def get_by_id(self, result_id: int) -> GradingResult | None:
        return self._db.get(GradingResult, result_id)

    def get_by_submission(self, submission_id: int) -> list[GradingResult]:
        return (
            self._db.query(GradingResult)
            .filter(GradingResult.submission_id == submission_id)
            .order_by(GradingResult.graded_at.desc())
            .all()
        )

    def get_pending_human_review(self) -> list[GradingResult]:
        return (
            self._db.query(GradingResult)
            .filter(GradingResult.needs_human_review == True)
            .order_by(GradingResult.graded_at)
            .all()
        )
