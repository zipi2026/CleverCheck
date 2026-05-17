from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT


class GradingService:

    def __init__(self, model):
        self.model    = model
        self.kw_model = KeyBERT(model=model)

    # ────────────────────────────────────────────
    # פונקציה ראשית — מחזירה את כל תוצאות הבדיקה
    # ────────────────────────────────────────────
    def grade_answer(self, student_answer, model_answer):

        # שלב א — חילוץ מושגים אוטומטי מתשובת המפתח
        key_concepts = self.extract_key_concepts(model_answer)

        # שלב ב — בדיקת כיסוי מושגים
        covered, missing = self.get_concept_coverage(
            student_answer, key_concepts
        )

        # שלב ג — ציון לפי מספר מושגים שכוסו
        if key_concepts:
            score = (len(covered) / len(key_concepts)) * 100
        else:
            score = 0

        # שלב ד — בדיקת שלילה
        has_negation = self.check_negation(student_answer)

        # שלב ה — קביעת סטטוס
        status = self._determine_status(score / 100, has_negation)

        # שלב ו — בדיקת מורה
        needs_review = self._needs_teacher_review(
            status, missing, has_negation
        )

        return {
            'score':         round(score, 2),
            'key_concepts':  key_concepts,
            'covered':       covered,
            'missing':       missing,
            'has_negation':  has_negation,
            'status':        status,
            'needs_review':  needs_review,
            'review_reason': self._get_review_reason(
                                 status, missing, has_negation
                             )
        }

    # ────────────────────────────────────────────
    # חילוץ מושגי מפתח מתשובת המפתח
    # ────────────────────────────────────────────
    def extract_key_concepts(self, model_answer, top_n=5):
        keywords = self.kw_model.extract_keywords(
            model_answer,
            keyphrase_ngram_range=(1, 2),
            top_n=top_n
        )

        concepts = [kw[0] for kw in keywords]

        # ניקוי — הסרת אותיות חיבור מתחילת ביטוי
        cleaned = []
        for concept in concepts:
            words    = concept.split()
            prefixes = ['ו', 'ה', 'מ', 'ב', 'ל', 'כ']
            if any(words[0].startswith(p) for p in prefixes):
                words[0] = words[0][1:]
            cleaned.append(' '.join(words))

        return cleaned

    # ────────────────────────────────────────────
    # בדיקת כיסוי — אילו מושגים כוסו ואילו חסרים
    # ────────────────────────────────────────────
    def get_concept_coverage(self, student_answer, key_concepts):
        if not key_concepts:
            return [], []

        student_segments = [
            s.strip() for s in student_answer.split('.')
            if s.strip()
        ]

        concept_embs = self.model.encode(
            key_concepts, convert_to_tensor=True
        )
        segment_embs = self.model.encode(
            student_segments, convert_to_tensor=True
        )

        scores          = util.cos_sim(concept_embs, segment_embs)
        max_per_concept = scores.max(dim=1).values

        covered = []
        missing = []

        for i, score in enumerate(max_per_concept):
            if score.item() >= 0.5:
                covered.append(key_concepts[i])
            else:
                missing.append(key_concepts[i])

        return covered, missing

    # ────────────────────────────────────────────
    # בדיקת שלילה של מושגים מרכזיים
    # ────────────────────────────────────────────
    def check_negation(self, text):
        critical_negations = [
            'אינו יעיל', 'לא יעיל', 'אין יעילות',
            'לא עובד',   'אינו פועל', 'לא נכון',
           'לא','אינו נכון', 'לא קשור',  'אינו קשור'
        ]
        return any(phrase in text for phrase in critical_negations)

    # ────────────────────────────────────────────
    # קביעת סטטוס לפי ציון ושלילה
    # ────────────────────────────────────────────
    def _determine_status(self, score, has_negation):
        if has_negation:
            return 'needs_llm_check'
        if score > 0.75:
            return 'accurate'
        if score > 0.4:
            return 'partial'
        return 'missing_concepts'

    # ────────────────────────────────────────────
    # האם לשלוח לבדיקת מורה?
    # ────────────────────────────────────────────
    def _needs_teacher_review(self, status, missing, has_negation):
        if has_negation:
            return True
        if status == 'partial':
            return True
        if len(missing) >= 2:
            return True
        return False

    # ────────────────────────────────────────────
    # סיבת בדיקת מורה
    # ────────────────────────────────────────────
    def _get_review_reason(self, status, missing, has_negation):
        if has_negation:
            return 'זוהתה שלילה — ייתכן שהתשובה שגויה'
        if status == 'partial':
            return 'תשובה חלקית — נדרשת בדיקה'
        if len(missing) >= 2:
            return f'חסרים {len(missing)} מושגים מרכזיים'
        return None