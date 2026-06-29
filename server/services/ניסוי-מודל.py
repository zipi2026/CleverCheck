import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_path = r"C:\git\CleverCheck\server\my_model\hebert_model_download (2)"

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
model.eval()


def build_input(question, teacher_answer, student_answer):
    return f"""[Q]{question}
[T]{teacher_answer}
[S]{student_answer}"""


def grade_answer(question, teacher_answer, student_answer):
    text = build_input(question, teacher_answer, student_answer)

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    with torch.no_grad():
        outputs = model(**inputs)

    score = outputs.logits.item()

    # אופציונלי: הגבלת טווח ל-0–1


    return score


# ---------------------------
# דוגמה לשימוש
# ---------------------------

question = "מה גורם ליום ולילה?"
teacher = "סיבוב כדור הארץ סביב צירו"
student = "הכבשה זזה ומסתובבת בעדינות סביב עצמה בסיבובים עגולים ויפים ונחמדים"

score = grade_answer(question, teacher, student)

print("Score:", round(score, 4))


if score < 0.3:
    print("שגוי")
elif score < 0.7:
    print("חלקי")
else:
    print("נכון")