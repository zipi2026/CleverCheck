"""
controllers/grading_controller.py — קבלת בקשות HTTP, validation, תגובה
"""
import logging
from flask import Blueprint, request, jsonify, Response

from dtos.dtos import GradeRequestDTO
from exceptions.exceptions import (
    ValidationError, ModelNotFoundError,
    GradingError, DatabaseError
)

logger = logging.getLogger(__name__)

grading_bp = Blueprint('grading', __name__, url_prefix='/api')


# ── Validation ────────────────────────────────────────────────
def _validate(data: dict) -> GradeRequestDTO:
    errors = []

    submission_id = data.get('submission_id')
    if submission_id is None or not isinstance(submission_id, int) or submission_id <= 0:
        errors.append("submission_id חייב להיות מספר שלם חיובי")

    student_answer = data.get('student_answer', '')
    if not student_answer or not isinstance(student_answer, str):
        errors.append("student_answer חסר או אינו מחרוזת")
    elif len(student_answer.strip()) < 3:
        errors.append("student_answer קצר מדי (מינימום 3 תווים)")

    key_concepts = data.get('key_concepts', [])
    if not isinstance(key_concepts, list) or len(key_concepts) == 0:
        errors.append("key_concepts חייב להיות רשימה לא ריקה")
    elif not all(isinstance(c, str) and len(c.strip()) > 0 for c in key_concepts):
        errors.append("כל מושג ב-key_concepts חייב להיות מחרוזת לא ריקה")

    if errors:
        raise ValidationError(" | ".join(errors))

    return GradeRequestDTO(
        submission_id=submission_id,
        student_answer=student_answer.strip(),
        key_concepts=[c.strip() for c in key_concepts],
    )


# ── Routes ────────────────────────────────────────────────────
def register_routes(grading_service):
    """
    מקבל את ה-service דרך DI (מ-app.py) ורושם את ה-routes.
    """

    @grading_bp.route('/grade', methods=['POST'])
    def grade() -> tuple[Response, int]:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "נדרש JSON body"}), 400

        try:
            dto      = _validate(data)
            response = grading_service.grade(dto)
            return jsonify(response.to_dict()), 200

        except ValidationError as e:
            logger.warning(f"Validation error: {e.message}")
            return jsonify({"error": e.message}), e.http_status

        except ModelNotFoundError as e:
            logger.error(f"Model error: {e.message}")
            return jsonify({"error": e.message}), e.http_status

        except (GradingError, DatabaseError) as e:
            logger.error(f"Service/DB error: {e.message}")
            return jsonify({"error": e.message}), e.http_status

        except Exception:
            logger.exception("Unexpected error in /grade")
            return jsonify({"error": "שגיאה פנימית בשרת"}), 500

    @grading_bp.route('/results/<int:result_id>', methods=['GET'])
    def get_result(result_id: int) -> tuple[Response, int]:
        try:
            result = grading_service._repo.get_by_id(result_id)
            if not result:
                return jsonify({"error": "תוצאה לא נמצאה"}), 404
            return jsonify({
                "id":                result.id,
                "submission_id":     result.submission_id,
                "final_score":       result.final_score,
                "confidence":        result.confidence,
                "needs_llm_review":  result.needs_llm_review,
                "needs_human_review": result.needs_human_review,
                "graded_at":         result.graded_at.isoformat(),
                "concepts": [
                    {
                        "concept":   c.concept,
                        "similarity": c.similarity,
                        "status":    c.status,
                    }
                    for c in result.concepts
                ]
            }), 200
        except Exception:
            logger.exception(f"Error fetching result {result_id}")
            return jsonify({"error": "שגיאה בשליפת תוצאה"}), 500

    return grading_bp
