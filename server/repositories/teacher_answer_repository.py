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
        return self.session.query(TeacherAnswer).filter_by(QuestionID=question_id).first()

    def delete(self, id):
        obj = self.session.query(TeacherAnswer).get(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj