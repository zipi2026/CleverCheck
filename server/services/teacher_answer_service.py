from server.models.teacher_answer import TeacherAnswer
from server.exceptions.exceptions import CleverCheckBaseError

class TeacherAnswerService:
    def __init__(self, repo):
        self.repo = repo

    def add_teacheranswer(self, dto):
        self.repo.add(TeacherAnswer(
            QuestionID=dto.QuestionID,
            AnswerText=dto.AnswerText,
            CorrectOptionID=dto.CorrectOptionID,
        ))

    def get_all_teacheranswers(self):
        return self.repo.get_all()

    def get_teacheranswer_by_id(self, teacher_answer_id):
        obj = self.repo.get_by_id(teacher_answer_id)
        if not obj:
            raise CleverCheckBaseError(teacher_answer_id)
        return obj

    def update_teacheranswer(self, teacher_answer_id, dto):
        obj = self.repo.update(teacher_answer_id, TeacherAnswer(
            QuestionID=dto.QuestionID,
            AnswerText=dto.AnswerText,
            CorrectOptionID=dto.CorrectOptionID,
        ))
        if not obj:
            raise CleverCheckBaseError(teacher_answer_id)
        return obj

    def delete_teacheranswer(self, teacher_answer_id):
        obj = self.repo.delete(teacher_answer_id)
        if not obj:
            raise CleverCheckBaseError(teacher_answer_id)
        return obj
