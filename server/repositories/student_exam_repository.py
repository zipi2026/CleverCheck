from server.models.student_exams import StudentExam
from sqlalchemy.orm import Session


class StudentExamRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: StudentExam):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_id(self, id):
        return self.session.get(StudentExam, id)

    def get_by_exam(self, exam_id):
        return (
            self.session.query(StudentExam)
            .filter_by(ExamID=exam_id)
            .all()
        )

    def get_by_student(self, student_id):
        return (
            self.session.query(StudentExam)
            .filter_by(StudentID=student_id)
            .all()
        )

    def delete(self, id):
        obj = self.session.get(StudentExam, id)

        if obj:
            self.session.delete(obj)
            self.session.commit()

        return obj