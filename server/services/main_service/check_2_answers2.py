from sentence_transformers import SentenceTransformer
from check_nagative_in_student_answer import contains_negation
from clean_student_answer import clean_student_answer
from key_words_teacher_answer import extract_teacher_keywords
from Synonym_reverso import SynonymClient
from typing import Dict
from keybert import KeyBERT
from typing import Dict
import stanza

# -------------------------
# הכנת מנוע Stanza
# -------------------------
# הפעם נשתמש במודול tokenize,mwt,pos,lemma
nlp = stanza.Pipeline(lang='he', processors='tokenize,mwt,pos,lemma')

# -------------------------
# פונקציות עזר
# -------------------------
def normalize_words(text: str) -> set:
    """
    מקבלת טקסט בעברית ומחזירה סט של מילים בצורת base form (lemma)
    """
    doc = nlp(text)
    lemmas = set()
    for sentence in doc.sentences:
        for word in sentence.words:
            lemmas.add(word.lemma)
    return lemmas


# -------------------------
# גרסת evaluate_answer
# -------------------------
def evaluate_answer(
        student_answer: str,
        teacher_answer: str,
        kw_model,
        synonym_client,
        max_score: float = 100
) -> Dict:
    """
    מחזירה:
    {
        score: float,
        matched_keywords: list,
        missing_keywords: list,
        negation_penalty: float
    }
    """

    # -------------------------
    # שלב 1 - ניקוי תשובת תלמיד
    # -------------------------
    cleaned_student = clean_student_answer(
        student_answer,
        kw_model
    )

    student_words = normalize_words(cleaned_student)

    # -------------------------
    # שלב 2 - מילות מפתח מורה
    # -------------------------
    teacher_keywords = extract_teacher_keywords(
        teacher_answer,
        kw_model
    )

    teacher_keywords = [kw[0] for kw in teacher_keywords]

    if not teacher_keywords:
        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "negation_penalty": 0
        }

    matched_keywords = []
    missing_keywords = []

    # -------------------------
    # שלב 3 - התאמת מושגים עם lemma
    # -------------------------
    for keyword in teacher_keywords:

        keyword_words = normalize_words(keyword)

        found = True

        for kw_word in keyword_words:

            direct_match = kw_word in student_words

            synonym_match = any(
                synonym_client.are_synonyms(
                    kw_word,
                    student_word
                )
                for student_word in student_words
            )

            if not (direct_match or synonym_match):
                found = False
                break

        if found:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    # -------------------------
    # שלב 4 - ציון בסיסי
    # -------------------------
    keyword_score = len(matched_keywords) / len(teacher_keywords)

    # -------------------------
    # שלב 5 - בדיקת שלילות
    # -------------------------
    teacher_negations = contains_negation(teacher_answer)
    student_negations = contains_negation(student_answer)

    negation_penalty = 0
    if bool(teacher_negations) != bool(student_negations):
        negation_penalty = 0.15

    # -------------------------
    # שלב 6 - חישוב ציון סופי
    # -------------------------
    final_score = max(0, keyword_score - negation_penalty)
    final_score *= max_score

    return {
        "score": round(final_score, 2),
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "negation_penalty": negation_penalty
    }