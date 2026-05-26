from server.models.exams import Exam
from sqlalchemy.orm import Session

class ExamRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: Exam):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(Exam).all()

    def get_by_id(self, id):
        return self.session.query(Exam).get(id)

    def update(self, id, new_data: Exam):
        obj = self.get_by_id(id)
        if obj:
            obj.ExamName = new_data.ExamName
            obj.TeacherID = new_data.TeacherID
            obj.SubjectID = new_data.SubjectID
            obj.StartTime = new_data.StartTime
            obj.EndTime = new_data.EndTime
            obj.DurationMinutes = new_data.DurationMinutes
            obj.Status = new_data.Status
            self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj