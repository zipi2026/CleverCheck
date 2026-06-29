from server.models.options import Option
from sqlalchemy.orm import Session


class OptionRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: Option):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_id(self, id):
        return self.session.get(Option, id)

    def get_by_question(self, question_id):
        return (
            self.session.query(Option)
            .filter_by(QuestionID=question_id)
            .all()
        )

    def update(self, id, new_data: Option):
        obj = self.get_by_id(id)

        if not obj:
            return None

        obj.OptionNumber = new_data.OptionNumber
        obj.QuestionID = new_data.QuestionID
        obj.OptionText = new_data.OptionText

        self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)

        if obj:
            self.session.delete(obj)
            self.session.commit()

        return obj

    def get_all(self):
        return self.session.query(Option).all()