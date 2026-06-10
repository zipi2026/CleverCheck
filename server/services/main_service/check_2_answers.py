from sentence_transformers import SentenceTransformer

from check_nagative_in_student_answer import contains_negation
from clean_student_answer import clean_student_answer
from key_words_teacher_answer import extract_teacher_keywords
from Synonym_reverso import SynonymClient
from typing import Dict, List
from keybert import KeyBERT

def prepare_teacher_keywords(teacher_answer: str, kw_model) -> List[str]:
    """
    מחזירה את רשימת מילות המפתח של המורה.
    פעולה זו מתבצעת פעם אחת בלבד.
    """
    teacher_keywords = extract_teacher_keywords(teacher_answer, kw_model)
    return [kw[0] for kw in teacher_keywords]

def evaluate_answer(
        student_answer: str,
        teacher_keywords: List[str],
        kw_model: KeyBERT,
        synonym_client: SynonymClient,
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
    #print("cleaned_student =", cleaned_student)

    student_words = set(cleaned_student.split())
    #print("student_words =", student_words)


    # -------------------------
    # שלב 2 - מילות מפתח מורה
    # -------------------------
    #teacher_keywords = extract_teacher_keywords(
       # teacher_answer,
      #  kw_model
   # )

    #teacher_keywords = [kw[0] for kw in teacher_keywords]
    #print("teacher_keywords =", teacher_keywords)

    if not teacher_keywords:
        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "negation_penalty": 0
        }

    matched_keywords = []
    missing_keywords = []
    print(teacher_keywords)

    all_words = set()
    for keyword in teacher_keywords:
        all_words.update(keyword.split())  # מוסיפים את כל המילים במילות המפתח

    all_words.update(student_words)  # מוסיפים את כל המילים בתשובת התלמיד

    for word in all_words:
        synonym_client.get_synonyms(word)

    # -------------------------
    # שלב 3 - התאמת מושגים
    # -------------------------
    all_words = set()
    for keyword in teacher_keywords:

        keyword_words = keyword.split()

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
            if (synonym_match and not direct_match):
                print("synonym****************************************************************")

            #if not (direct_match or synonym_match):
            if not (direct_match):
                found = False
                break

        if found:
            # print("keyword =", keyword)
            # print("keyword_words =", keyword_words)
            # print("student_words =", student_words)
            # print("found =", found)
            # print("-" * 50)
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    # -------------------------
    # שלב 4 - ציון בסיסי
    # -------------------------
    keyword_score = (
        len(matched_keywords) /
        len(teacher_keywords)
    )
    # print("matched_keywords =", matched_keywords)
    # print("missing_keywords =", missing_keywords)

    # -------------------------
    # שלב 5 - בדיקת שלילות
    # -------------------------
    teacher_negations = contains_negation(
        teacher_answer
    )

    student_negations = contains_negation(
        student_answer
    )

    negation_penalty = 0

    if bool(teacher_negations) != bool(student_negations):
        negation_penalty = 0.15

    # -------------------------
    # שלב 6 - חישוב ציון סופי
    # -------------------------
    final_score = max(
        0,
        keyword_score - negation_penalty
    )

    final_score *= max_score

    return {
        "score": round(final_score, 2),
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "negation_penalty": negation_penalty
    }
if __name__ == "__main__":
    model = SentenceTransformer(
        r"C:\Users\kuperbergz\PycharmProjects\CleverCheck\server\my_model"
    )
    kw_model = KeyBERT(model=model)

    teacher_answer = "מנהלת את משאבי המחשב"

    test_answers = [

        # התאמה מלאה כמעט
        "מערכת ההפעלה מנהלת את משאבי המחשב",

        # ניסוח אחר
        "מערכת ההפעלה אחראית לניהול משאבי המחשב",

        # שינוי סדר מילים
        "את משאבי המחשב מנהלת מערכת ההפעלה",

        # חסרה מילה אחת
        "מערכת ההפעלה מנהלת משאבים",

        # רק חלק מהרעיון
        "מערכת ההפעלה מנהלת את המחשב",

        # שימוש במילה קרובה
        "מערכת ההפעלה שולטת במשאבי המחשב",

        # שימוש במילה קרובה נוספת
        "מערכת ההפעלה אחראית על משאבי המחשב",

        # תשובה קצרה מאוד
        "ניהול משאבי מחשב",

        # מושג אחד בלבד
        "מערכת הפעלה",

        # מושג אחר מהתחום
        "מערכת ההפעלה מפעילה תוכנות",

        # תשובה חלקית
        "משאבי המחשב מנוהלים על ידי מערכת ההפעלה",

        # ניסוח פסיבי
        "ניהול משאבי המחשב מתבצע באמצעות מערכת ההפעלה",

        # הרחבה מעבר לנדרש
        "מערכת ההפעלה מנהלת את משאבי המחשב ואת תהליכי הריצה",

        # מילים מיותרות
        "לדעתי מערכת ההפעלה אחראית על כל משאבי המחשב",

        # טעות מושגית
        "מערכת ההפעלה מייצרת את משאבי המחשב",

        # הפוך מהתשובה
        "מערכת ההפעלה אינה מנהלת את משאבי המחשב",

        # שלילה עקיפה
        "לא מערכת ההפעלה מנהלת את משאבי המחשב",

        # תשובה לא קשורה
        "המחשב מחובר לאינטרנט",

        # תשובה ריקה כמעט
        "מחשב",

        # תשובה ארוכה
        "מערכת ההפעלה היא תוכנה מרכזית האחראית לניהול משאבי המחשב, הזיכרון, המעבד והקבצים",

        # נרדפות אפשריות
        "מערכת ההפעלה אחראית על הקצאת משאבי המחשב",

        # נרדפות אפשריות
        "מערכת ההפעלה מפקחת על משאבי המחשב",

        # כתיב מעט שונה
        "מערכת הפעלה מנהלת משאבי מחשב",

        # ללא המושג המרכזי
        "ניהול זיכרון ומעבד",

        # מושגים נכונים חלקית
        "מערכת ההפעלה מנהלת זיכרון ומעבד",

        # תשובה שגויה
        "הדפדפן מנהל את משאבי המחשב"
    ]
    question = "מה תפקידו של מסד נתונים?"

    teacher_answer2 = "מסד נתונים משמש לאחסון וניהול מידע."

    test_answers2 = [
        # התאמה מלאה
        "מסד נתונים משמש לאחסון וניהול מידע.",

        # שינוי סדר מילים
        "ניהול ואחסון מידע מתבצע באמצעות מסד נתונים.",

        # ניסוח אחר
        "מסד הנתונים אחראי לשמור ולנהל מידע.",
        "מסד נתונים מאפשר לשמור מידע ולנהל אותו.",
        "מסד נתונים מרכז את המידע ומנהל אותו.",

        # מילים נרדפות
        "מסד נתונים משמש לשמירת נתונים וניהולם.",
        "מסד הנתונים מאחסן מידע ומטפל בו.",
        "מסד נתונים מרכז נתונים ומאפשר ניהול שלהם.",
        "מערכת בסיס נתונים מיועדת לאחסון מידע.",

        # תשובות חלקיות
        "מסד נתונים מאחסן מידע.",
        "מסד נתונים מנהל מידע.",
        "שמירת נתונים.",
        "אחסון מידע.",

        # הרחבה נכונה
        "מסד נתונים משמש לאחסון, ניהול ושליפה של מידע.",
        "מסד הנתונים שומר מידע ומאפשר חיפוש ועדכון שלו.",
        "מסד נתונים מרכז את כל הנתונים ומאפשר גישה מסודרת אליהם.",

        # תשובות עם משמעות דומה אך מילים שונות
        "המערכת שומרת נתונים בצורה מאורגנת.",
        "מאגר הנתונים מאפשר תחזוקה ושליטה על מידע.",
        "הנתונים נשמרים בצורה מסודרת וניתנים לניהול.",
        "המערכת מרכזת מידע ומאפשרת לעבוד איתו ביעילות.",

        # תשובות שגויות
        "מסד נתונים מריץ תוכניות.",
        "מסד נתונים הוא מערכת הפעלה.",
        "מסד נתונים מיועד רק להצגת מידע.",
        "מסד נתונים מחליף את המעבד.",

        # שלילה
        "מסד נתונים אינו משמש לאחסון מידע.",
        "מסד נתונים לא מנהל מידע.",

        # תשובות לא קשורות
        "הדפדפן מציג אתרי אינטרנט.",
        "המעבד מבצע חישובים.",
        "הזיכרון שומר נתונים זמניים."
    ]

    kw_model = KeyBERT(model=model)
    teacher_keywords = prepare_teacher_keywords(teacher_answer2, kw_model)

    for answer in test_answers2:
        result = evaluate_answer(
            student_answer=answer,
            teacher_keywords=teacher_keywords,
            kw_model=kw_model,
            synonym_client=SynonymClient()
        )
        print("Student:", answer)
        print("Result :", result)
        print("=" * 80)