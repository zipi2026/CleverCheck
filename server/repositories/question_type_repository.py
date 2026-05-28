from server.models.question_types import QuestionType
from sqlalchemy.orm import Session


class QuestionTypeRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: QuestionType):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(QuestionType).all()

    def get_by_id(self, id):
        return self.session.get(QuestionType, id)

    def update(self, id, new_data: QuestionType):
        obj = self.get_by_id(id)

        if not obj:
            return None

        obj.type_name = new_data.type_name
        self.session.commit()

        return obj

    def delete(self, id):
        obj = self.get_by_id(id)

        if obj:
            self.session.delete(obj)
            self.session.commit()

        return obj