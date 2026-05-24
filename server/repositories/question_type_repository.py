from server.models.question_type import QuestionType
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
        return self.session.query(QuestionType).get(id)

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj