from server.models.student_exams import StudentExam
from server.exceptions.exceptions import CleverCheckBaseError

class StudentExamService:
    def __init__(self, repo):
        self.repo = repo

    def add_studentexam(self, dto):
        self.repo.add(StudentExam(
            ExamID=dto.ExamID,
            StudentID=dto.StudentID,
            StartTime=dto.StartTime,
            EndTime=dto.EndTime,
            Score=dto.Score,
        ))

    def get_all_studentexams(self):
        return self.repo.get_all()

    def get_studentexam_by_id(self, student_exam_id):
        obj = self.repo.get_by_id(student_exam_id)
        if not obj:
            raise CleverCheckBaseError(student_exam_id)
        return obj

    def update_studentexam(self, student_exam_id, dto):
        obj = self.repo.update(student_exam_id, StudentExam(
            ExamID=dto.ExamID,
            StudentID=dto.StudentID,
            StartTime=dto.StartTime,
            EndTime=dto.EndTime,
            Score=dto.Score,
        ))
        if not obj:
            raise CleverCheckBaseError(student_exam_id)
        return obj

    def delete_studentexam(self, student_exam_id):
        obj = self.repo.delete(student_exam_id)
        if not obj:
            raise CleverCheckBaseError(student_exam_id)
        return obj
