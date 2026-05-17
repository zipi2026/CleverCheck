import os
from sentence_transformers import SentenceTransformer
from services.grading_service import GradingService

# ── טעינת המודל ──────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'my_model')
model      = SentenceTransformer(MODEL_PATH)

# ── יצירת service ─────────────────────────────────────────
grading_service = GradingService(model=model)

# ── נתוני בדיקה ───────────────────────────────────────────
model_answer = "האלגוריתם יעיל מבחינת סיבוכיות זמן וצריכת זיכרון."

test_cases = [
    {
        'name':    'תשובה מלאה ונכונה',
        'student': 'האלגוריתם יעיל מבחינת זמן ריצה וזיכרון.',
    },
    {
        'name':    'תשובה עם שלילה',
        #'student': 'האלגוריתם אינו יעיל ואינו חוסך זיכרון.',
        'student': 'האלגוריתם לא חוסך זיכרון.',
#'student': 'האלגוריתם לא חוסך זיכרון.',
    },
    {
        'name':    'תשובה חלקית',
        'student': 'האלגוריתם חוסך זיכרון.',
    },
    {
        'name':    'תשובה לא קשורה',
        'student': 'הכלב רץ בשדה.',
    },
    {
        'name':    'תשובה במילים שונות אבל נכונה',
        'student': 'הפתרון מהיר ולא צורך הרבה משאבים.',
    },
]

# ── הרצת הבדיקות ──────────────────────────────────────────
print("=" * 55)
print("        בדיקות מערכת CleverCheck")
print("=" * 55)
print(f"תשובת מפתח: {model_answer}")
print("=" * 55)

for case in test_cases:
    result = grading_service.grade_answer(
        case['student'],
        model_answer
    )

    print(f"\n--- {case['name']} ---")
    print(f"תשובת תלמיד:   {case['student']}")
    print(f"ציון:           {result['score']}")
    print(f"סטטוס:          {result['status']}")
    print(f"מושגים שחולצו: {result['key_concepts']}")
    print(f"מושגים חסרים:  {result['missing']}")
    print(f"שלילה:          {result['has_negation']}")
    print(f"בדיקת מורה:    {result['needs_review']}")
    print(f"סיבה:           {result['review_reason']}")
    print("-" * 55)