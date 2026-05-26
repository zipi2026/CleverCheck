from server.models.student import Student
from server.exceptions.exceptions import CleverCheckBaseError

class StudentService:
    def __init__(self, repo):
        self.repo = repo

    def add_student(self, dto):
        self.repo.add(Student(
            FirstName=dto.FirstName,
            LastName=dto.LastName,
            PasswordHash=dto.PasswordHash,
            ClassID=dto.ClassID,
            IsActive=dto.IsActive,
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
            FirstName=dto.FirstName,
            LastName=dto.LastName,
            PasswordHash=dto.PasswordHash,
            ClassID=dto.ClassID,
            IsActive=dto.IsActive,
        ))
        if not obj:
            raise CleverCheckBaseError(student_id)
        return obj

    def delete_student(self, student_id):
        obj = self.repo.delete(student_id)
        if not obj:
            raise CleverCheckBaseError(student_id)
        return obj
