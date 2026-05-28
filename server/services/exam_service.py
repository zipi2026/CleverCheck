from server.models.exams import Exam
from server.exceptions.exceptions import CleverCheckBaseError


class ExamService:
    def __init__(self, repo):
        self.repo = repo

    def add_exam(self, dto):
        self.repo.add(
            Exam(
                exam_name=dto.ExamName,
                teacher_id=dto.TeacherID,
                start_time=dto.StartTime,
                end_time=dto.EndTime,
                duration_minutes=dto.DurationMinutes,
                status=dto.Status,
            )
        )

    def get_all_exams(self):
        return self.repo.get_all()

    def get_exam_by_id(self, exam_id):
        obj = self.repo.get_by_id(exam_id)
        if not obj:
            raise CleverCheckBaseError(exam_id)
        return obj

    def update_exam(self, exam_id, dto):
        obj = self.repo.update(
            exam_id,
            Exam(
                exam_name=dto.ExamName,
                teacher_id=dto.TeacherID,
                start_time=dto.StartTime,
                end_time=dto.EndTime,
                duration_minutes=dto.DurationMinutes,
                status=dto.Status,
            )
        )

        if not obj:
            raise CleverCheckBaseError(exam_id)

        return obj

    def delete_exam(self, exam_id):
        obj = self.repo.delete(exam_id)
        if not obj:
            raise CleverCheckBaseError(exam_id)
        return obj