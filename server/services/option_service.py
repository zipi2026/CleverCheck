from server.models.options import Option
from server.exceptions.exceptions import CleverCheckBaseError


class OptionService:
    def __init__(self, repo):
        self.repo = repo

    def add_option(self, dto):
        self.repo.add(
            Option(
                option_number=dto.OptionNumber,
                question_id=dto.QuestionID,
                option_text=dto.OptionText,
            )
        )

    def get_all_options(self):
        return self.repo.get_all()

    def get_option_by_id(self, option_id):
        obj = self.repo.get_by_id(option_id)
        if not obj:
            raise CleverCheckBaseError(option_id)
        return obj

    def update_option(self, option_id, dto):
        obj = self.repo.update(
            option_id,
            Option(
                option_number=dto.OptionNumber,
                question_id=dto.QuestionID,
                option_text=dto.OptionText,
            )
        )

        if not obj:
            raise CleverCheckBaseError(option_id)

        return obj

    def delete_option(self, option_id):
        obj = self.repo.delete(option_id)
        if not obj:
            raise CleverCheckBaseError(option_id)
        return obj