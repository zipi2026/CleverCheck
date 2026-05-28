from server.models.student_answer import StudentAnswer
from sqlalchemy.orm import Session

class StudentAnswerRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: StudentAnswer):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(StudentAnswer).all()

    def get_by_id(self, id):
        return self.session.get(StudentAnswer, id)

    def get_by_exam(self, student_exam_id):
        return self.session.query(StudentAnswer)\
            .filter_by(student_exam_id=student_exam_id)\
            .all()

    def update(self, id, new_data: StudentAnswer):
        obj = self.get_by_id(id)
        if not obj:
            return None

        obj.student_exam_id = new_data.student_exam_id
        obj.question_id = new_data.question_id
        obj.answer_text = new_data.answer_text
        obj.selected_option_id = new_data.selected_option_id
        obj.score = new_data.score

        self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj