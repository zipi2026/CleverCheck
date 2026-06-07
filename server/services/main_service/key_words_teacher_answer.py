from typing import List
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer


def extract_teacher_keywords(teacher_answer: str, kw_model: KeyBERT, threshold: float = 0.65) -> List[str]:

    keywords = kw_model.extract_keywords(
        teacher_answer,
        keyphrase_ngram_range=(1,2),
        top_n=20,
        use_mmr = True,  # מקדם מגוונות
        diversity = 0.7  # עד כמה המילים שונות זו מזו
    )

    #concepts = [kw for kw in keywords]

    # cleaned = []
    # for concept in concepts:
    #     words = concept.split()
    #     prefixes = ['ו', 'ה', 'מ', 'ב', 'ל', 'כ']
    #     if words and any(words[0].startswith(p) for p in prefixes):
    #         words[0] = words[0][1:]
    #     cleaned.append(' '.join(words))

    filtered = [kw for kw in keywords if kw[1] >= threshold]
    return filtered


# ──────────────────────────────
# דוגמת הרצה
# ──────────────────────────────
if __name__ == "__main__":
    model = SentenceTransformer(r"/server/my_model")
    kw_model = KeyBERT(model=model)

    sentences = [
        "הגורם המרכזי לשינוי האקלים הוא פליטת גזי חממה על ידי האדם.",
        "המים מחממים את פני השטח בעזרת קרינת השמש.",
        "כדי לבצע חישוב מסוים, יש להשתמש בנוסחה המתאימה.",
        "הצמח צורך אור כדי לבצע פוטוסינתזה.",
        "הכוח הפועל על הגוף שווה למסתו כפול תאוצתו.",
        "ההתחממות הגלובלית נגרמת בעיקר על ידי פליטות גזי חממה.",
        "מהפכת התעשייה הביאה לשינויים כלכליים וחברתיים במאה ה-18.",
        "המהפכה הצרפתית גרמה להפלת המלוכה ולעליית הרפובליקה.",
        "הקולוניאליזם האירופי השפיע על מבנה המדינות באפריקה ובאסיה.",
        "מלחמת העולם הראשונה גרמה לשינויים גיאופוליטיים גדולים באירופה.",
        "הקמת האומות המאוחדות נועדה לשמור על שלום עולמי אחרי מלחמת העולם השנייה."
    ]
    qa_pairs = [
        {"question": "מה הייתה המהפכה התעשייתית?", "answer": "פיתוח מכונות ושינויים חברתיים"},
        {"question": "מה גרם למלחמת העולם הראשונה?", "answer": "בריתות צבאיות ותחרות כלכלית"},
        {"question": "מה הייתה המהפכה הצרפתית?", "answer": "הפלת המלוכה ועליית הרפובליקה"},
        {"question": "מה הייתה השפעת הקולוניאליזם האירופי?", "answer": "השפעה על מדינות באפריקה ובאסיה"},
        {"question": "מהי מטרת הקמת האומות המאוחדות?", "answer": "שמירה על שלום עולמי"},
        {"question": "מהי מלחמת העולם השנייה?", "answer": "קונפליקט עולמי 1939–1945"},
        {"question": "מהי מהפכת המידע?", "answer": "מחשבים ואינטרנט"},
        {"question": "מה הייתה המהפכה הרוסית?", "answer": "הפלת הצאר ושלטון קומוניסטי"},
        {"question": "מהי המלחמה הקרה?", "answer": "מירוץ חימוש והשפעה פוליטית"},
        {"question": "מה הייתה מהפכת 1848 באירופה?", "answer": "מרידות ושינויים פוליטיים"}
    ]

    for qa in qa_pairs:
        keywords = extract_teacher_keywords(qa["answer"], kw_model)
        print(f"Question: {qa['question']}")
        print(f"Answer: {qa['answer']}")
        print(f"Keywords: {keywords}\n")
