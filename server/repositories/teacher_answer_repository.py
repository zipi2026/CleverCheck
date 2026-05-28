from server.models.teacher_answer import TeacherAnswer
from sqlalchemy.orm import Session

class TeacherAnswerRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: TeacherAnswer):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_question(self, question_id):
        return self.session.query(TeacherAnswer).filter_by(question_id=question_id).first()

    def delete(self, id):
        obj = self.session.get(TeacherAnswer, id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj

    def get_by_id(self, id):
        return self.session.get(TeacherAnswer, id)

    def update(self, id, new_data):
        obj = self.session.get(TeacherAnswer, id)

        if not obj:
            return None

        obj.question_id = new_data.question_id
        obj.answer_text = new_data.answer_text
        obj.correct_option_id = new_data.correct_option_id

        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(TeacherAnswer).all()