import re

# ────────────── מילים נפוצות ונרדפות ──────────────
STOPWORDS = ['ה', 'ו', 'של', 'על', 'עם', 'את', 'כי', 'אם', 'ל', 'ב']

# מילים נרדפות
SYNONYMS = {
    'זריחה': ['התחלה'],
    'שקיעה': ['סיום'],
    'מהיר': ['זריז', 'מהר'],
    'חוסך': ['חוסן']
}

# הפכים בסיסיים
ANTONYMS = {
    'מזרח': ['מערב'],
    'מערב': ['מזרח'],
    'שורש': ['קצה'],
}

NEGATIONS = ['לא', 'אין', 'אינו', 'בלי', 'אינה', 'אינם']

# ────────────── פונקציות עזר ──────────────
def normalize(text):
    """ניקוי, המרה לאותיות קטנות והסרת מילים נפוצות"""
    text = text.lower()
    words = re.findall(r'\w+', text)
    words = [w for w in words if w not in STOPWORDS]
    return words

def expand_synonyms_and_antonyms(words):
    """מוסיף מילים נרדפות והפכים"""
    expanded = set()
    for w in words:
        expanded.add(w)
        if w in SYNONYMS:
            expanded.update(SYNONYMS[w])
        if w in ANTONYMS:
            expanded.update(ANTONYMS[w])  # לצורך חיתוך/בדיקה
    return expanded

def contains_negation(text):
    """בודק אם יש שלילה במשפט"""
    return any(neg in text for neg in NEGATIONS)

# ────────────── חישוב דמיון ──────────────
def sentence_similarity(sent1, sent2):
    words1 = normalize(sent1)
    words2 = normalize(sent2)

    words1_exp = expand_synonyms_and_antonyms(words1)
    words2_exp = expand_synonyms_and_antonyms(words2)

    intersection = words1_exp & words2_exp
    union = words1_exp | words2_exp

    similarity = len(intersection) / len(union) if union else 0

    # בדיקה של שלילה — הופכת את המשמעות
    neg1 = contains_negation(sent1)
    neg2 = contains_negation(sent2)
    if neg1 != neg2:
        similarity *= 0.1  # לא אפס מוחלט, אבל מאוד מוריד

    return similarity

# ────────────── דוגמה ──────────────
s1 = "השמש זורחת במזרח"
s2 = "הכיוון של זריחת השמש הוא ממזרח"
s3 = "השמש אינה זורחת במזרח"  # הפוכה
s4 = "השמש זורחת במערב"       # הפוכה לחלוטין

print("דמיון s1 ↔ s2:", sentence_similarity(s1, s2))  # גבוה
print("דמיון s1 ↔ s3:", sentence_similarity(s1, s3))  # נמוך
print("דמיון s1 ↔ s4:", sentence_similarity(s1, s4))  # נמוך מאוד