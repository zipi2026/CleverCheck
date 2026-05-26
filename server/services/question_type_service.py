from server.models.question_types import QuestionType
from server.exceptions.exceptions import CleverCheckBaseError

class QuestionTypeService:
    def __init__(self, repo):
        self.repo = repo

    def add_questiontype(self, dto):
        self.repo.add(QuestionType(
            TypeName=dto.TypeName,
        ))

    def get_all_questiontypes(self):
        return self.repo.get_all()

    def get_questiontype_by_id(self, question_type_id):
        obj = self.repo.get_by_id(question_type_id)
        if not obj:
            raise CleverCheckBaseError(question_type_id)
        return obj

    def update_questiontype(self, question_type_id, dto):
        obj = self.repo.update(question_type_id, QuestionType(
            TypeName=dto.TypeName,
        ))
        if not obj:
            raise CleverCheckBaseError(question_type_id)
        return obj

    def delete_questiontype(self, question_type_id):
        obj = self.repo.delete(question_type_id)
        if not obj:
            raise CleverCheckBaseError(question_type_id)
        return obj
