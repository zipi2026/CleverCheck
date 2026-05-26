from server.models.student_answer import StudentAnswer
from server.exceptions.exceptions import CleverCheckBaseError

class StudentAnswerService:
    def __init__(self, repo):
        self.repo = repo

    def add_studentanswer(self, dto):
        self.repo.add(StudentAnswer(
            StudentExamID=dto.StudentExamID,
            QuestionID=dto.QuestionID,
            AnswerText=dto.AnswerText,
            SelectedOptionID=dto.SelectedOptionID,
            Score=dto.Score,
        ))

    def get_all_studentanswers(self):
        return self.repo.get_all()

    def get_studentanswer_by_id(self, student_answer_id):
        obj = self.repo.get_by_id(student_answer_id)
        if not obj:
            raise CleverCheckBaseError(student_answer_id)
        return obj

    def update_studentanswer(self, student_answer_id, dto):
        obj = self.repo.update(student_answer_id, StudentAnswer(
            StudentExamID=dto.StudentExamID,
            QuestionID=dto.QuestionID,
            AnswerText=dto.AnswerText,
            SelectedOptionID=dto.SelectedOptionID,
            Score=dto.Score,
        ))
        if not obj:
            raise CleverCheckBaseError(student_answer_id)
        return obj

    def delete_studentanswer(self, student_answer_id):
        obj = self.repo.delete(student_answer_id)
        if not obj:
            raise CleverCheckBaseError(student_answer_id)
        return obj
