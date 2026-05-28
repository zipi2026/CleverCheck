import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("./my_model")


NEGATIONS = {"לא", "אין", "אסור", "מותר", "בלתי", "נגד"}

def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^\u0590-\u05FFa-zA-Z0-9\s]", "", text)
    return text


def get_embedding_score(a, b):
    emb = model.encode([a, b], normalize_embeddings=True)
    return cosine_similarity([emb[0]], [emb[1]])[0][0]


def keyword_score(a, b):
    a_words = set(a.split())
    b_words = set(b.split())

    if not a_words or not b_words:
        return 0

    return len(a_words & b_words) / len(a_words | b_words)


def negation_penalty(a, b):
    a_set = set(a.split())
    b_set = set(b.split())

    a_neg = any(w in NEGATIONS for w in a_set)
    b_neg = any(w in NEGATIONS for w in b_set)

    if a_neg != b_neg:
        return 0.4  # ענישה על סתירה
    return 1.0


def final_score(teacher, student):
    teacher = normalize(teacher)
    student = normalize(student)

    emb = get_embedding_score(teacher, student)
    key = keyword_score(teacher, student)
    neg = negation_penalty(teacher, student)

    # משקולות
    score = (
        emb * 0.7 +
        key * 0.2 +
        emb * key * 0.1
    )

    score *= neg

    # נרמול ל-0-100
    score = max(0, min(1, score)) * 100

    # שיפור התאמה כמעט זהה
    if score > 97:
        return 100

    return round(score)