from server.models.student_answer import StudentAnswer
from server.exceptions.exceptions import CleverCheckBaseError

class StudentAnswerService:
    def __init__(self, repo):
        self.repo = repo

    def add_student_answer(self, dto):
        return self.repo.add(StudentAnswer(
            student_exam_id=dto.student_exam_id,
            question_id=dto.question_id,
            answer_text=dto.answer_text,
            selected_option_id=dto.selected_option_id,
            score=dto.score,
        ))

    def get_all_student_answers(self):
        return self.repo.get_all()

    def get_student_answer_by_id(self, student_answer_id):
        obj = self.repo.get_by_id(student_answer_id)
        if not obj:
            raise CleverCheckBaseError(student_answer_id)
        return obj

    def update_student_answer(self, student_answer_id, dto):
        obj = self.repo.update(student_answer_id, StudentAnswer(
            student_exam_id=dto.student_exam_id,
            question_id=dto.question_id,
            answer_text=dto.answer_text,
            selected_option_id=dto.selected_option_id,
            score=dto.score,
        ))
        if not obj:
            raise CleverCheckBaseError(student_answer_id)
        return obj

    def delete_student_answer(self, student_answer_id):
        obj = self.repo.delete(student_answer_id)
        if not obj:
            raise CleverCheckBaseError(student_answer_id)
        return obj