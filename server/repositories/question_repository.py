from server.models.questions import Question
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
        return self.session.get(Question, id)

    def update(self, id, new_data: Question):
        obj = self.get_by_id(id)

        if not obj:
            return None

        obj.question_text = new_data.question_text
        obj.question_type_id = new_data.question_type_id
        obj.max_score = new_data.max_score

        self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)

        if obj:
            self.session.delete(obj)
            self.session.commit()

        return obj