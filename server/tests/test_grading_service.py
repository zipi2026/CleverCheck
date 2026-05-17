"""
tests/test_grading_service.py — בדיקות יחידה לשכבת Service
מריץ ללא SQL Server ובלי מודל אמיתי (mocks מלאים)
"""
import pytest
from unittest.mock import MagicMock, patch

# ── Mocking כבד לפני import ───────────────────────────────────
# מונע טעינת torch / sentence_transformers בזמן בדיקות
import sys, types

# stub: torch
torch_stub = types.ModuleType('torch')
torch_stub.cuda = MagicMock()
torch_stub.cuda.is_available = MagicMock(return_value=False)
sys.modules['torch'] = torch_stub

# stub: sentence_transformers
st_stub = types.ModuleType('sentence_transformers')
st_stub.SentenceTransformer = MagicMock()
st_stub.util = MagicMock()
sys.modules['sentence_transformers'] = st_stub
sys.modules['sentence_transformers.util'] = st_stub.util

# עכשיו בטוח לייבא
from dtos.dtos import GradeRequestDTO, ConceptEvaluationDTO
from exceptions.exceptions import ValidationError, GradingError, ModelNotFoundError


# ══════════════════════════════════════════════════════════════
# 1. בדיקות לפונקציות עזר של עברית
# ══════════════════════════════════════════════════════════════
class TestHebrewHelpers:

    def setup_method(self):
        # ייבוא מאוחר אחרי stub
        from services import grading_service as gs
        self.gs = gs

    def test_clean_word_removes_punctuation(self):
        assert self.gs._clean_word("פולימורפיזם,") == "פולימורפיזם"
        assert self.gs._clean_word(".מחלקה.") == "מחלקה"

    def test_is_concept_match_exact(self):
        assert self.gs._is_concept_match("פולימורפיזם", "פולימורפיזם")

    def test_is_concept_match_with_prefix_heh(self):
        assert self.gs._is_concept_match("הפולימורפיזם", "פולימורפיזם")

    def test_is_concept_match_with_prefix_vav(self):
        assert self.gs._is_concept_match("ובפולימורפיזם", "פולימורפיזם") is False  # 'וב' לא ב-HEBREW_PREFIXES

    def test_is_concept_match_no_match(self):
        assert not self.gs._is_concept_match("ירושת", "פולימורפיזם")

    def test_check_negation_direct(self):
        assert self.gs._check_negation("פולימורפיזם לא קיים בג'אווה", "פולימורפיזם") is True

    def test_check_negation_before_concept(self):
        assert self.gs._check_negation("לא ניתן להשתמש בפולימורפיזם כאן", "פולימורפיזם") is True

    def test_check_negation_absent(self):
        assert self.gs._check_negation("פולימורפיזם מאפשר גמישות", "פולימורפיזם") is False

    def test_split_segments_basic(self):
        segs = self.gs._split_segments("משפט ראשון. משפט שני. משפט שלישי.")
        assert len(segs) == 3

    def test_split_segments_newlines(self):
        segs = self.gs._split_segments("שורה א\nשורה ב\nשורה ג")
        assert len(segs) == 3

    def test_split_segments_short_removed(self):
        segs = self.gs._split_segments("א. תשובה ארוכה מספיק.")
        assert all(len(s) > 2 for s in segs)

    def test_confidence_low_borderline(self):
        assert self.gs._confidence(0.60) == "low"

    def test_confidence_high_above(self):
        assert self.gs._confidence(0.90) == "high"

    def test_confidence_high_below(self):
        assert self.gs._confidence(0.20) == "high"


# ══════════════════════════════════════════════════════════════
# 2. בדיקות GradingService עם מודל מדומה
# ══════════════════════════════════════════════════════════════
class TestGradingService:

    def _make_service(self, sim_scores: list[float]):
        """בונה GradingService עם מודל מדומה שמחזיר ציוני דמיון מוגדרים."""
        import torch as _torch

        repo = MagicMock()
        saved_mock = MagicMock()
        saved_mock.id = 42
        repo.save_result.return_value = saved_mock

        # patch get_model ו-util.cos_sim
        with patch('services.grading_service.get_model') as mock_get_model, \
             patch('services.grading_service.util') as mock_util:

            import torch
            # mock: cos_sim מחזיר מטריצה שורה-אחת לכל מושג
            mock_tensor = MagicMock()
            mock_tensor.max.return_value = (
                MagicMock(
                    __getitem__=lambda self, i: MagicMock(item=lambda: sim_scores[i])
                ),
                MagicMock(
                    __getitem__=lambda self, i: MagicMock(item=lambda: 0)
                ),
            )
            mock_util.cos_sim.return_value = mock_tensor
            mock_get_model.return_value.encode.return_value = MagicMock()

            from services.grading_service import GradingService
            return GradingService(repo), repo

    def test_all_concepts_found(self):
        repo = MagicMock()
        saved = MagicMock(); saved.id = 1
        repo.save_result.return_value = saved

        with patch('services.grading_service.get_model') as mgm, \
             patch('services.grading_service.util') as mu:

            # כל מושג מקבל ציון 0.9 → נמצא
            scores = [0.9, 0.9]
            max_tensor = MagicMock()
            max_tensor.__getitem__ = lambda s, i: MagicMock(item=lambda: scores[i])
            idx_tensor = MagicMock()
            idx_tensor.__getitem__ = lambda s, i: MagicMock(item=lambda: 0)
            mu.cos_sim.return_value.max.return_value = (max_tensor, idx_tensor)
            mgm.return_value.encode.return_value = MagicMock()

            from services.grading_service import GradingService
            svc = GradingService(repo)
            dto = GradeRequestDTO(
                submission_id=1,
                student_answer="פולימורפיזם הוא עיקרון של תכנות מונחה עצמים. הוא מאפשר גמישות.",
                key_concepts=["פולימורפיזם", "גמישות"],
            )
            result = svc.grade(dto)
            assert result.score == 100.0
            assert result.confidence == "high"
            assert not result.needs_llm_review

    def test_empty_concepts_returns_full_score(self):
        repo = MagicMock()
        saved = MagicMock(); saved.id = 2
        repo.save_result.return_value = saved

        with patch('services.grading_service.get_model'), \
             patch('services.grading_service.util'):
            from services.grading_service import GradingService
            svc = GradingService(repo)
            dto = GradeRequestDTO(1, "תשובה כלשהי", [])
            result = svc.grade(dto)
            assert result.score == 100.0

    def test_model_not_found_raises(self):
        repo = MagicMock()
        with patch('services.grading_service.get_model',
                   side_effect=ModelNotFoundError("לא נמצא")):
            from services.grading_service import GradingService
            svc = GradingService(repo)
            dto = GradeRequestDTO(1, "תשובה", ["מושג"])
            with pytest.raises(ModelNotFoundError):
                svc.grade(dto)


# ══════════════════════════════════════════════════════════════
# 3. בדיקות DTO
# ══════════════════════════════════════════════════════════════
class TestDTOs:

    def test_concept_dto_to_dict(self):
        dto = ConceptEvaluationDTO(
            concept="ירושה",
            similarity=0.85,
            best_segment="ירושה מאפשרת שימוש חוזר בקוד",
            negation_detected=False,
            status="correct",
        )
        d = dto.to_dict()
        assert d["concept"] == "ירושה"
        assert d["similarity"] == 0.85
        assert d["status"] == "correct"

    def test_grade_request_dto_fields(self):
        dto = GradeRequestDTO(
            submission_id=99,
            student_answer="תשובה לדוגמה",
            key_concepts=["מושג א", "מושג ב"],
        )
        assert dto.submission_id == 99
        assert len(dto.key_concepts) == 2


# ══════════════════════════════════════════════════════════════
# 4. בדיקות Validation (דרך Controller)
# ══════════════════════════════════════════════════════════════
class TestValidation:

    def setup_method(self):
        from controllers.grading_controller import _validate
        self.validate = _validate

    def test_valid_input_passes(self):
        data = {
            "submission_id": 1,
            "student_answer": "תשובה תקינה לגמרי",
            "key_concepts": ["מושג"],
        }
        dto = self.validate(data)
        assert dto.submission_id == 1

    def test_missing_answer_raises(self):
        data = {"submission_id": 1, "key_concepts": ["מושג"]}
        with pytest.raises(ValidationError):
            self.validate(data)

    def test_empty_concepts_raises(self):
        data = {"submission_id": 1, "student_answer": "תשובה", "key_concepts": []}
        with pytest.raises(ValidationError):
            self.validate(data)

    def test_invalid_submission_id_raises(self):
        data = {"submission_id": -5, "student_answer": "תשובה", "key_concepts": ["מ"]}
        with pytest.raises(ValidationError):
            self.validate(data)

    def test_short_answer_raises(self):
        data = {"submission_id": 1, "student_answer": "א", "key_concepts": ["מושג"]}
        with pytest.raises(ValidationError):
            self.validate(data)
