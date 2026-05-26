from server.models.options import Option
from sqlalchemy.orm import Session

class OptionRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: Option):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_question(self, question_id):
        return self.session.query(Option).filter_by(QuestionID=question_id).all()

    def delete(self, id):
        obj = self.session.query(Option).get(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj