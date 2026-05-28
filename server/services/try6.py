from sentence_transformers import CrossEncoder
import re

# מודל Cross-Encoder רב-לשוני (כולל עברית)
model = CrossEncoder("cross-encoder/stsb-xlm-r-multilingual")


# -----------------------------
# ניקוי טקסט
# -----------------------------
def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\u0590-\u05FFa-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


# -----------------------------
# זיהוי שלילה / סתירה
# -----------------------------
NEGATIONS = {
    "לא", "אין", "אסור", "מותר", "בלי", "נגד", "אינו", "אינה", "אינם"
}


def has_negation(text: str) -> bool:
    words = set(text.split())
    return any(w in NEGATIONS for w in words)


# -----------------------------
# חפיפת מילים (keywords)
# -----------------------------
def keyword_similarity(a: str, b: str) -> float:
    a_words = set(a.split())
    b_words = set(b.split())

    if not a_words or not b_words:
        return 0.0

    return len(a_words & b_words) / len(a_words | b_words)


# -----------------------------
# Cross Encoder score
# -----------------------------
def cross_score(a: str, b: str) -> float:
    score = model.predict([(a, b)])[0]
    score = float(score)

    # נרמול אם המודל מחזיר טווח 0–5
    if score > 1:
        score = score / 5.0

    return max(0.0, min(1.0, score))


# -----------------------------
# ציון סופי משולב
# -----------------------------
def grade_answer(teacher: str, student: str) -> int:
    teacher = normalize(teacher)
    student = normalize(student)

    if not teacher or not student:
        return 0

    # 1. Cross Encoder (הכי חשוב)
    ce = cross_score(teacher, student)

    # 2. Keywords
    kw = keyword_similarity(teacher, student)

    # 3. שלילה
    teacher_neg = has_negation(teacher)
    student_neg = has_negation(student)

    neg_penalty = 1.0
    if teacher_neg != student_neg:
        neg_penalty = 0.35  # ענישה על סתירה

    # -----------------------------
    # שילוב משוקלל
    # -----------------------------
    score = (
        ce * 0.75 +
        kw * 0.20 +
        ce * kw * 0.05
    )

    score *= neg_penalty

    # נרמול ל-0–100
    score = max(0.0, min(1.0, score)) * 100

    # שיפור דיוק לתשובות זהות כמעט לחלוטין
    if score >= 97:
        return 100

    return round(score)


# -----------------------------
# דוגמאות הרצה
# -----------------------------
if __name__ == "__main__":

    tests = [
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

    for t, s in tests:
        print("Teacher:", t)
        print("Student:", s)
        print("Score:", grade_answer(t, s))
        print("-" * 40)