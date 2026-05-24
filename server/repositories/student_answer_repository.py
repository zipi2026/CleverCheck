from server.models.student_answer import StudentAnswer
from sqlalchemy.orm import Session

class StudentAnswerRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: StudentAnswer):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_exam(self, student_exam_id):
        return self.session.query(StudentAnswer).filter_by(StudentExamID=student_exam_id).all()

    def delete(self, id):
        obj = self.session.query(StudentAnswer).get(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj