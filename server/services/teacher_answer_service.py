from server.models.teacher_answer import TeacherAnswer
from server.exceptions.exceptions import CleverCheckBaseError

class TeacherAnswerService:
    def __init__(self, repo):
        self.repo = repo

    def add_teacher_answer(self, dto):
        self.repo.add(TeacherAnswer(
           question_id=dto.question_id,
           answer_text=dto.answer_text,
           correct_option_id=dto.correct_option_id,
        ))

    def get_all_teacher_answers(self):
        return self.repo.get_all()

    def get_teacher_answer_by_id(self, teacher_answer_id):
        obj = self.repo.get_by_id(teacher_answer_id)
        if not obj:
            raise CleverCheckBaseError(teacher_answer_id)
        return obj

    def update_teacher_answer(self, teacher_answer_id, dto):
        obj = self.repo.update(teacher_answer_id, TeacherAnswer(
           question_id=dto.question_id,
           answer_text=dto.answer_text,
           correct_option_id=dto.correct_option_id,
        ))
        if not obj:
            raise CleverCheckBaseError(teacher_answer_id)
        return obj

    def delete_teacher_answer(self, teacher_answer_id):
        obj = self.repo.delete(teacher_answer_id)
        if not obj:
            raise CleverCheckBaseError(teacher_answer_id)
        return obj
