from server.models.question import Question
from sqlalchemy.orm import Session

class QuestionRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: Question):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(Question).all()

    def get_by_id(self, id):
        return self.session.query(Question).get(id)

    def update(self, id, new_data: Question):
        obj = self.get_by_id(id)
        if obj:
            obj.QuestionText = new_data.QuestionText
            obj.QuestionTypeID = new_data.QuestionTypeID
            obj.MaxScore = new_data.MaxScore
            self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj