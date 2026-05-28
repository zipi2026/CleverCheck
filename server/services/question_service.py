from server.models.questions import Question
from server.exceptions.exceptions import CleverCheckBaseError


class QuestionService:
    def __init__(self, repo):
        self.repo = repo

    def add_question(self, dto):
        self.repo.add(
            Question(
                question_number=dto.QuestionNumber,
                exam_id=dto.ExamID,
                question_text=dto.QuestionText,
                question_type_id=dto.QuestionTypeID,
                max_score=dto.MaxScore,
            )
        )

    def get_all_questions(self):
        return self.repo.get_all()

    def get_question_by_id(self, question_id):
        obj = self.repo.get_by_id(question_id)
        if not obj:
            raise CleverCheckBaseError(question_id)
        return obj

    def update_question(self, question_id, dto):
        obj = self.repo.update(
            question_id,
            Question(
                question_number=dto.QuestionNumber,
                exam_id=dto.ExamID,
                question_text=dto.QuestionText,
                question_type_id=dto.QuestionTypeID,
                max_score=dto.MaxScore,
            )
        )

        if not obj:
            raise CleverCheckBaseError(question_id)

        return obj

    def delete_question(self, question_id):
        obj = self.repo.delete(question_id)
        if not obj:
            raise CleverCheckBaseError(question_id)
        return obj