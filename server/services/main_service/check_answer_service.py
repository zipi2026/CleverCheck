from typing import List
import re
from keybert import KeyBERT
from server.services.main_service.Synonym_reverso import SynonymClient
from sentence_transformers import SentenceTransformer


class CleverCheckService:
    def __init__(self):
        self.model = SentenceTransformer(r"/server/my_model")  # מתאים גם לעברית
        self.kw_model = KeyBERT(model=self.model)
        self.syn_client = SynonymClient()

    # ──────────────────────────────
    # 1. חילוץ מילות מפתח מהמורה
    # ──────────────────────────────
    def extract_teacher_keywords(self, teacher_answer: str, top_n: int = 5) -> List[str]:
        keywords = self.kw_model.extract_keywords(
            teacher_answer,
            keyphrase_ngram_range=(1,2),
            top_n=top_n
        )
        concepts = [kw[0] for kw in keywords]

        cleaned = []
        for concept in concepts:
            words = concept.split()
            prefixes = ['ו', 'ה', 'מ', 'ב', 'ל', 'כ']
            if words and any(words[0].startswith(p) for p in prefixes):
                words[0] = words[0][1:]
            cleaned.append(' '.join(words))
        return cleaned

    # ──────────────────────────────
    # 2. ניקוי תשובת תלמיד
    # ──────────────────────────────
    def clean_student_answer(self, student_answer: str) -> List[str]:
        # הסרת רווחים וסימני פיסוק
        text = " ".join([line.strip() for line in student_answer.splitlines() if line])
        text = re.sub(r"[^\w\s\u0590-\u05FF]", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        # הסרת מילים לא משמעותיות
        stopwords = {
            "אני","אתה","את","הוא","היא","אנחנו","אתם","אתן",
            "שלי","שלך","שלו","שלה","שלנו","שלכם","שלכן",
            "זה","זו","אלה","אילו",
            "עם","על","אל","מאז","עד","עליו",
            "אבל","או","אם","כי","כאשר","כל","גם","יותר","פחות",
            "האם","בין","כך","גם כן","אחרי",
            "מה","מי","שהוא","שהיא","שהם","שהן","מן",
            "בעד","תוך","מתוך","אצל","לפני",
            "לצד","עבור","למען","תחת","על-ידי","כדי"
        }
        words = [word for word in text.split() if word not in stopwords]
        cleaned_text = " ".join(words)

        # חילוץ מילות מפתח עיקריות
        keywords = self.kw_model.extract_keywords(
            cleaned_text,
            keyphrase_ngram_range=(1,2),
            top_n=5
        )
        return [kw[0] for kw in keywords]

    # ──────────────────────────────
    # 3. בדיקת מילים נרדפות
    # ──────────────────────────────
    def are_synonyms(self, word1: str, word2: str) -> bool:
        return self.syn_client.are_synonyms(word1, word2)

    # ──────────────────────────────
    # 4. בדיקת שלילה
    # ──────────────────────────────
    @staticmethod
    def contains_negation(text: str) -> List[int]:
        negations = {"לא","אין","אינו","אינה","אינם","אינן","בלי","שום","אף","חסר","אסור"}
        return [i for i, word in enumerate(text.split()) if word in negations]

    # ──────────────────────────────
    # פונקציה ראשית – חישוב ציון
    # ──────────────────────────────
    def evaluate_answer(self, teacher_answer: str, student_answer: str) -> float:
        teacher_keywords = self.extract_teacher_keywords(teacher_answer)
        student_keywords = self.clean_student_answer(student_answer)

        # בדיקה סמנטית: חפיפה עם מילים נרדפות
        matched = 0
        for t_word in teacher_keywords:
            for s_word in student_keywords:
                if t_word == s_word or self.are_synonyms(t_word, s_word):
                    matched += 1
                    break

        # בדיקת שלילה
        teacher_neg = self.contains_negation(teacher_answer)
        student_neg = self.contains_negation(student_answer)
        neg_penalty = 0
        if bool(teacher_neg) != bool(student_neg):
            neg_penalty = 0.2  # 20% ירידה בציון אם השלילה לא תואמת

        # חישוב ציון סופי
        score = (matched / max(len(teacher_keywords), 1))  # אחוז מילות מפתח
        score = max(0.0, score - neg_penalty)
        return round(score * 100, 2)  # ציון מ-0 עד 100%

# ──────────────────────────────
# דוגמת שימוש
# ──────────────────────────────
if __name__ == "__main__":
    service = CleverCheckService()
    teacher_answer = "הגורם העיקרי לשינוי האקלים הוא פליטת גזי חממה על ידי האדם."
    student_answer = "האדם אחראי לפליטת גזי חממה וזה משנה את האקלים."
    score = service.evaluate_answer(teacher_answer, student_answer)
    print(f"ציון התלמיד: {score}%")