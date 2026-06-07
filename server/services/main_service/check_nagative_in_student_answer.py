from typing import List


@staticmethod
def contains_negation(text: str) -> List[int]:
    negations = {"לא", "אין", "אינו", "אינה", "אינם", "אינן", "בלי", "שום", "אף", "חסר", "אסור"}
    return [i for i, word in enumerate(text.split()) if word in negations]


if __name__ == "__main__":
    texts = [
        "אין לי מחשב אבל לא חסר לי כלום",
        "אין לי מחשב",
        "המחשב עובד תקין",
        "אסור למחוק את הקובץ",
        "לא ניתן להתחבר לשרת"
    ]

    for text in texts:
        result = contains_negation(text)
        print(f"{text} -> {result}")