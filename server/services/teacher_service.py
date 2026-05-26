from server.models.teachers import Teacher
from server.exceptions.exceptions import CleverCheckBaseError

class TeacherService:
    def __init__(self, repo):
        self.repo = repo

    def add_teacher(self, dto):
        self.repo.add(Teacher(
            FirstName=dto.FirstName,
            LastName=dto.LastName,
            Email=dto.Email,
            PasswordHash=dto.PasswordHash,
            IsActive=dto.IsActive,
            Role=dto.Role,
        ))

    def get_all_teachers(self):
        return self.repo.get_all()

    def get_teacher_by_id(self, teacher_id):
        obj = self.repo.get_by_id(teacher_id)
        if not obj:
            raise CleverCheckBaseError(teacher_id)
        return obj

    def update_teacher(self, teacher_id, dto):
        obj = self.repo.update(teacher_id, Teacher(
            FirstName=dto.FirstName,
            LastName=dto.LastName,
            Email=dto.Email,
            PasswordHash=dto.PasswordHash,
            IsActive=dto.IsActive,
            Role=dto.Role,
        ))
        if not obj:
            raise CleverCheckBaseError(teacher_id)
        return obj

    def delete_teacher(self, teacher_id):
        obj = self.repo.delete(teacher_id)
        if not obj:
            raise CleverCheckBaseError(teacher_id)
        return obj
