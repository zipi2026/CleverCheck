from server.models.student import Student
from server.exceptions.exceptions import CleverCheckBaseError

class StudentService:
    def __init__(self, repo):
        self.repo = repo

    def add_student(self, dto):
        self.repo.add(Student(
            first_name=dto.first_name,
            last_name = dto.last_name,
            class_id = dto.class_id,
            password_hash=dto.password_hash,
            is_active = dto.is_active,
        ))

    def get_all_students(self):
        return self.repo.get_all()

    def get_student_by_id(self, student_id):
        obj = self.repo.get_by_id(student_id)
        if not obj:
            raise CleverCheckBaseError(student_id)
        return obj

    def update_student(self, student_id, dto):
        obj = self.repo.update(student_id, Student(
            first_name=dto.first_name,
            last_name = dto.last_name,
            class_id = dto.class_id,
            password_hash=dto.password_hash,
            is_active = dto.is_active,
        ))
        if not obj:
            raise CleverCheckBaseError(student_id)
        return obj

    def delete_student(self, student_id):
        obj = self.repo.delete(student_id)
        if not obj:
            raise CleverCheckBaseError(student_id)
        return obj
