import re
from keybert import KeyBERT
from server.services.Synonym_reverso import SynonymClient

class TextProcessingService:
    def __init__(self, model):
        self.model = model  # SentenceTransformer – משמש ל-KeyBERT ולבדיקת כיסוי מושגים
        self.kw_model = KeyBERT(model=model)  # מודל ל-KeyBERT עם אותו SentenceTransformer

    # ────────────────────────────────────────────
    # חיפוש מיקומי המילים השליליות
    # ────────────────────────────────────────────
    @staticmethod
    def contains_negation(text: str) -> list[int]:
        negations = {
            "לא", "אין", "אינו", "אינה", "אינם", "אינן",
            "בלי", "שום",  "אף", "חסר", "אסור"
        }
        negation_positions = []

        split_text = text.split()
        for i, word in enumerate(split_text):
            if word in negations:
                negation_positions.append(i)

        return negation_positions

    # ────────────────────────────────────────────
    # חילוץ מושגי מפתח מתשובת המודל
    # ────────────────────────────────────────────
    def extract_key_concepts(self, text, top_n=5):
        keywords = self.kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            top_n=top_n
        )
        concepts = [kw[0] for kw in keywords]

        # ניקוי — הסרת אותיות חיבור מתחילת ביטוי
        cleaned = []
        for concept in concepts:
            words = concept.split()
            prefixes = ['ו', 'ה', 'מ', 'ב', 'ל', 'כ']
            if any(words[0].startswith(p) for p in prefixes):
                words[0] = words[0][1:]
            cleaned.append(' '.join(words))

        return cleaned

    # ────────────────────────────────────────────
    # ניקוי הטקסט
    # ────────────────────────────────────────────
    @staticmethod
    def clean_text(self, text: str):
        # הסרת רווחים בתחילת/סוף שורות
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]
        text = " ".join(lines)

        # המרת כמה רווחים לרווח אחד
        text = re.sub(r"\s+", " ", text)

        # הסרת סימני פיסוק ותווים מיוחדים
        text = re.sub(r"[^\w\s\u0590-\u05FF]", "", text)
        text = re.sub(r"[^\x00-\x7F\u0590-\u05FF]", "", text)
        text = re.sub(r"[^a-zA-Z0-9\u0590-\u05FF\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        # רשימת מילות יחס וקישור
        stopwords = {
            "אני", "אתה", "את", "הוא", "היא", "אנחנו", "אתם", "אתן",
            "שלי", "שלך", "שלו", "שלה", "שלנו", "שלכם", "שלכן",
            "זה", "זו", "אלה", "אילו",
            "עם", "על", "אל", "מאז", "עד", "עליו",
            "אבל", "או", "אם", "כי", "כאשר", "כל", "גם", "יותר", "פחות",
            "האם", "בין", "כך", "גם כן", "אחרי",
            "מה", "מי", "שהוא", "שהיא", "שהם", "שהן", "מן",
            "בעד", "תוך", "מתוך", "אצל", "לפני",
            "לצד", "עבור", "למען", "תחת", "על-ידי", "כדי",
        }

        words = text.split()
        words = [word for word in words if word not in stopwords]
        cleaned_text = " ".join(words)

        return self.extract_key_concepts(cleaned_text)

    # ────────────────────────────────────────────
    # בדיקה אם שתי מילים נרדפות
    # ────────────────────────────────────────────
    def are_concepts_synonyms(self, word1: str, word2: str) -> bool:
        return SynonymClient.are_synonyms(word1, word2)

