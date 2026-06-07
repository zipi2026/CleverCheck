# ──────────────────────────────
# 2. ניקוי תשובת תלמיד
# ──────────────────────────────
import re
from typing import List
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer


def clean_student_answer(student_answer: str,kw_model: KeyBERT) -> List[str]:
    # הסרת רווחים וסימני פיסוק
    #print("Original student answer:", student_answer)
    text = " ".join([line.strip() for line in student_answer.splitlines() if line])
    text = re.sub(r"[^\w\s\u0590-\u05FF]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # הסרת מילים לא משמעותיות
    stopwords = {
        "אני", "אתה", "את", "הוא", "היא", "אנחנו", "אתם", "אתן",
        "שלי", "שלך", "שלו", "שלה", "שלנו", "שלכם", "שלכן",
        "זה", "זו", "אלה", "אילו",
        "עם", "על", "אל", "מאז", "עד", "עליו",
        "אבל", "או", "אם", "כי", "כאשר", "כל", "גם", "יותר", "פחות",
        "האם", "בין", "כך", "גם כן", "אחרי",
        "מה", "מי", "שהוא", "שהיא", "שהם", "שהן", "מן",
        "בעד", "תוך", "מתוך", "אצל", "לפני",
        "לצד", "עבור", "למען", "תחת", "על-ידי", "כדי"
    }
    words = [word for word in text.split() if word not in stopwords]
    cleaned_text = " ".join(words)
    # print("Original student answer:", student_answer)
    # print("Cleaned student text:", text)
    # print("Words after stopwords removal:", words)
    return cleaned_text

    # חילוץ מילות מפתח עיקריות
    # keywords = kw_model.extract_keywords(
    #     cleaned_text,
    #     keyphrase_ngram_range=(1, 2),
    #     top_n=5
    # )
    # return [kw[0] for kw in keywords]

# ──────────────────────────────
# הרצה
# ──────────────────────────────

if __name__ == "__main__":
    model = SentenceTransformer(r"/server/my_model")
    kw_model = KeyBERT(model=model)

    sentences = [
        "מערכת ההפעלה מנהלת את משאבי המחשב",
        "מסד נתונים מאפשר אחסון ושליפה של מידע",
        "פרוטוקול HTTP משמש להעברת מידע באינטרנט"
    ]

    for sentence in sentences:
        result = clean_student_answer(sentence, kw_model)
        print(f"משפט: {sentence}")
        print(f"מילות מפתח: {result}")
        print("-" * 40)