import os

base_path = "server/services"

services = {
    "class_service.py": {
        "model": "Class",
        "dto": "ClassDTO",
        "repo": "ClassRepository",
        "pk": "class_id",
        "fields": ["ClassName"]
    },
    "teacher_service.py": {
        "model": "Teacher",
        "dto": "TeacherDTO",
        "repo": "TeacherRepository",
        "pk": "teacher_id",
        "fields": ["FirstName", "LastName", "Email", "PasswordHash", "IsActive", "Role"]
    },
    "student_service.py": {
        "model": "Student",
        "dto": "StudentDTO",
        "repo": "StudentRepository",
        "pk": "student_id",
        "fields": ["FirstName", "LastName", "PasswordHash", "ClassID", "IsActive"]
    },
    "exam_service.py": {
        "model": "Exam",
        "dto": "ExamDTO",
        "repo": "ExamRepository",
        "pk": "exam_id",
        "fields": ["ExamName", "TeacherID",  "StartTime", "EndTime", "DurationMinutes", "Status"]
    },
    "question_service.py": {
        "model": "Question",
        "dto": "QuestionDTO",
        "repo": "QuestionRepository",
        "pk": "question_id",
        "fields": ["QuestionNumber", "ExamID", "QuestionText", "QuestionTypeID", "MaxScore"]
    },
    "option_service.py": {
        "model": "Option",
        "dto": "OptionDTO",
        "repo": "OptionRepository",
        "pk": "option_id",
        "fields": ["OptionNumber", "QuestionID", "OptionText"]
    },
    "question_type_service.py": {
        "model": "QuestionType",
        "dto": "QuestionTypeDTO",
        "repo": "QuestionTypeRepository",
        "pk": "question_type_id",
        "fields": ["TypeName"]
    },
    "teacher_answer_service.py": {
        "model": "TeacherAnswer",
        "dto": "TeacherAnswerDTO",
        "repo": "TeacherAnswerRepository",
        "pk": "teacher_answer_id",
        "fields": ["QuestionID", "AnswerText", "CorrectOptionID"]
    },
    "student_exam_service.py": {
        "model": "StudentExam",
        "dto": "StudentExamDTO",
        "repo": "StudentExamRepository",
        "pk": "student_exam_id",
        "fields": ["ExamID", "StudentID", "StartTime", "EndTime", "Score"]
    },
    "student_answer_service.py": {
        "model": "StudentAnswer",
        "dto": "StudentAnswerDTO",
        "repo": "StudentAnswerRepository",
        "pk": "student_answer_id",
        "fields": ["StudentExamID", "QuestionID", "AnswerText", "SelectedOptionID", "Score"]
    }
}

template = """from server.models.{model_lower} import {model}
from server.exceptions.exceptions import CleverCheckBaseError

class {service_name}:
    def __init__(self, repo):
        self.repo = repo

    def add_{model_lower}(self, dto):
        self.repo.add({model}(
{create_fields}
        ))

    def get_all_{model_lower}s(self):
        return self.repo.get_all()

    def get_{model_lower}_by_id(self, {pk}):
        obj = self.repo.get_by_id({pk})
        if not obj:
            raise CleverCheckBaseError({pk})
        return obj

    def update_{model_lower}(self, {pk}, dto):
        obj = self.repo.update({pk}, {model}(
{update_fields}
        ))
        if not obj:
            raise CleverCheckBaseError({pk})
        return obj

    def delete_{model_lower}(self, {pk}):
        obj = self.repo.delete({pk})
        if not obj:
            raise CleverCheckBaseError({pk})
        return obj
"""

os.makedirs(base_path, exist_ok=True)

for file_name, cfg in services.items():
    model = cfg["model"]
    model_lower = model.lower()
    pk = cfg["pk"]

    service_name = model + "Service"

    create_fields = "\n".join([f"            {f}=dto.{f}," for f in cfg["fields"]])
    update_fields = create_fields

    content = template.format(
        model=model,
        model_lower=model_lower,
        service_name=service_name,
        create_fields=create_fields,
        update_fields=update_fields,
        pk=pk
    )

    with open(os.path.join(base_path, file_name), "w", encoding="utf-8") as f:
        f.write(content)

print("FULL SERVICES GENERATED SUCCESSFULLY")