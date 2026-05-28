# pip install sentence-transformers scikit-learn torch transformers

import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "my_model")

model = SentenceTransformer(MODEL_PATH)
# מודל רב-לשוני חזק עם תמיכה טובה בעברית
#MODEL_NAME = "intfloat/multilingual-e5-large"

#model = SentenceTransformer(MODEL_NAME)
#model = SentenceTransformer("./my_model")

NEGATION_WORDS = {
    "לא",
    "אין",
    "אינו",
    "אינה",
    "אינם",
    "אינן",
    "בלי",
    "מלבד",
    "נגד",
    "אסור",
    "אף",
}

def normalize_hebrew(text: str) -> str:
    text = text.strip().lower()

    # הסרת ניקוד
    text = re.sub(r"[\u0591-\u05C7]", "", text)

    # ניקוי תווים
    text = re.sub(r"[^\u0590-\u05FFa-zA-Z0-9\s]", " ", text)

    # רווחים כפולים
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_negation(text: str) -> bool:
    words = set(text.split())
    return any(word in words for word in NEGATION_WORDS)


def semantic_similarity_score(teacher_answer: str, student_answer: str) -> int:
    """
    מחזיר ציון בין 0 ל-100 לפי דמיון סמנטי בעברית.
    """

    teacher = normalize_hebrew(teacher_answer)
    student = normalize_hebrew(student_answer)

    if not teacher or not student:
        return 0

    # embeddings
    embeddings = model.encode(
        [teacher, student],
        normalize_embeddings=True
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # המרה לטווח 0-100
    #score = max(0.0, min(1.0, float(similarity)))
    #score = score * 100
    score = max(0.0, min(1.0, float(similarity)))

    # המרה חכמה לציון אנושי
    if score >= 0.97:
        final_score = 100
    elif score >= 0.93:
        final_score = 95 + ((score - 0.93) / 0.04) * 5
    elif score >= 0.85:
        final_score = 80 + ((score - 0.85) / 0.08) * 15
    elif score >= 0.70:
        final_score = 50 + ((score - 0.70) / 0.15) * 30
    else:
        final_score = score * 70

    score = final_score

    # טיפול בשלילה הפוכה
    teacher_neg = contains_negation(teacher)
    student_neg = contains_negation(student)

    if teacher_neg != student_neg:
        # אם יש דמיון גבוה אבל שלילה הפוכה -> הורדה חדה
        if score > 70:
            score *= 0.15
        else:
            score *= 0.4

    # בונוס להתאמה כמעט זהה
    if teacher == student:
        score = 100

    return int(round(score))


# =========================
# דוגמאות
# =========================

examples = [
    (
        "ירושלים היא עיר הבירה של ישראל",
        "בירת ישראל היא ירושלים"
    ),
    (
        "מים רותחים בטמפרטורה של 100 מעלות",
        "מים קופאים ב0 מעלות"
    ),
    (
        "אסור להדליק אש בשבת",
        "מותר להדליק אש בשבת"
    ),
]

for t, s in examples:
    print("Teacher :", t)
    print("Student :", s)
    print("Score   :", semantic_similarity_score(t, s))
    print("-" * 50)