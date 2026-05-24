import os

BASE_PATH = "repositories"

files = [
    "class_repository.py",
    "teacher_repository.py",
    "student_repository.py",
    "subject_repository.py",
    "exam_repository.py",
    "question_repository.py",
    "option_repository.py",
    "question_type_repository.py",
    "teacher_answer_repository.py",
    "student_exam_repository.py",
    "student_answer_repository.py",
]

template = """from sqlalchemy.orm import Session

class {name}Repository:
    def __init__(self, session: Session):
        self.session = session
"""

os.makedirs(BASE_PATH, exist_ok=True)

for file in files:
    class_name = file.replace(".py", "").replace("_repository", "").title().replace("_", "")
    content = template.format(name=class_name)

    with open(os.path.join(BASE_PATH, file), "w", encoding="utf-8") as f:
        f.write(content)

print("Repositories created successfully.")