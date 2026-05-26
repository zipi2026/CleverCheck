"""
tests/test_grading_controller.py — בדיקות אינטגרציה ל-Controller
"""
import pytest
import sys
import types
from unittest.mock import MagicMock
from flask import Flask, Blueprint, request, jsonify

# ── stubs ─────────────────────────────────────────────────────
torch_stub = types.ModuleType('torch')
torch_stub.cuda = MagicMock()
torch_stub.cuda.is_available = MagicMock(return_value=False)
sys.modules['torch'] = torch_stub

st_stub = types.ModuleType('sentence_transformers')
st_stub.SentenceTransformer = MagicMock()
st_stub.util = MagicMock()
sys.modules['sentence_transformers'] = st_stub
sys.modules['sentence_transformers.util'] = st_stub.util


def _build_app(mock_service):
    """בונה Flask app עם Blueprint חדש לכל קריאה."""
    from server.dtos.dtos import GradeResponseDTO, ConceptEvaluationDTO
    from server.exceptions.exceptions import (
        ValidationError, GradingError, DatabaseError, ModelNotFoundError
    )
    from server.controllers.grading_controller import _validate

    app = Flask(__name__)
    app.config['TESTING'] = True

    bp = Blueprint(f'grading_{id(mock_service)}', __name__, url_prefix='/api')

    @bp.route('/grade', methods=['POST'])
    def grade():
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "נדרש JSON body"}), 400
        try:
            dto = _validate(data)
            response = mock_service.grade(dto)
            return jsonify(response.to_dict()), 200
        except ValidationError as e:
            return jsonify({"error": e.message}), e.http_status
        except ModelNotFoundError as e:
            return jsonify({"error": e.message}), e.http_status
        except (GradingError, DatabaseError) as e:
            return jsonify({"error": e.message}), e.http_status
        except Exception:
            return jsonify({"error": "שגיאה פנימית"}), 500

    @bp.route('/results/<int:result_id>', methods=['GET'])
    def get_result(result_id):
        result = mock_service._repo.get_by_id(result_id)
        if not result:
            return jsonify({"error": "לא נמצא"}), 404
        return jsonify({"id": result.id, "submission_id": result.submission_id}), 200

    app.register_blueprint(bp)
    return app


@pytest.fixture
def client():
    from server.dtos.dtos import GradeResponseDTO, ConceptEvaluationDTO

    mock_service = MagicMock()
    mock_service.grade.return_value = GradeResponseDTO(
        grading_result_id=1,
        submission_id=10,
        score=75.0,
        confidence="low",
        needs_llm_review=True,
        needs_human_review=False,
        breakdown=[
            ConceptEvaluationDTO(
                concept="פולימורפיזם",
                similarity=0.75,
                best_segment="פולימורפיזם הוא עיקרון",
                negation_detected=False,
                status="correct",
            )
        ],
    )
    app = _build_app(mock_service)
    with app.test_client() as c:
        yield c, mock_service


# ══════════════════════════════════════════════════════════════
class TestGradeEndpoint:

    def test_valid_request_returns_200(self, client):
        c, _ = client
        resp = c.post('/api/grade', json={
            "submission_id": 10,
            "student_answer": "פולימורפיזם מאפשר גמישות בתכנות",
            "key_concepts": ["פולימורפיזם"],
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["score"] == 75.0
        assert data["confidence"] == "low"
        assert data["needs_llm_review"] is True

    def test_missing_body_returns_400(self, client):
        c, _ = client
        resp = c.post('/api/grade', data="not json",
                      content_type='application/json')
        assert resp.status_code == 400

    def test_missing_student_answer_returns_400(self, client):
        c, _ = client
        resp = c.post('/api/grade', json={
            "submission_id": 1,
            "key_concepts": ["מושג"],
        })
        assert resp.status_code == 400

    def test_empty_concepts_returns_400(self, client):
        c, _ = client
        resp = c.post('/api/grade', json={
            "submission_id": 1,
            "student_answer": "תשובה ארוכה מספיק",
            "key_concepts": [],
        })
        assert resp.status_code == 400

    def test_invalid_submission_id_returns_400(self, client):
        c, _ = client
        resp = c.post('/api/grade', json={
            "submission_id": -1,
            "student_answer": "תשובה ארוכה מספיק",
            "key_concepts": ["מושג"],
        })
        assert resp.status_code == 400

    def test_service_exception_returns_500(self, client):
        from server.exceptions.exceptions import GradingError
        c, mock_service = client
        mock_service.grade.side_effect = GradingError("שגיאה פנימית")
        resp = c.post('/api/grade', json={
            "submission_id": 1,
            "student_answer": "תשובה מספיק ארוכה",
            "key_concepts": ["מושג"],
        })
        assert resp.status_code == 500

    def test_response_contains_breakdown(self, client):
        c, _ = client
        resp = c.post('/api/grade', json={
            "submission_id": 10,
            "student_answer": "פולימורפיזם הוא גמישות",
            "key_concepts": ["פולימורפיזם"],
        })
        data = resp.get_json()
        assert "breakdown" in data
        assert len(data["breakdown"]) == 1
        assert data["breakdown"][0]["concept"] == "פולימורפיזם"


# ══════════════════════════════════════════════════════════════
class TestGetResultEndpoint:

    def test_existing_result_returns_200(self, client):
        c, mock_service = client
        fake = MagicMock()
        fake.id = 1
        fake.submission_id = 10
        mock_service._repo.get_by_id.return_value = fake
        resp = c.get('/api/results/1')
        assert resp.status_code == 200

    def test_missing_result_returns_404(self, client):
        c, mock_service = client
        mock_service._repo.get_by_id.return_value = None
        resp = c.get('/api/results/999')
        assert resp.status_code == 404
