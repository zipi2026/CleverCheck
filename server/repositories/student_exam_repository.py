from server.models import StudentExam


class StudentExamRepository:
    def __init__(self, session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        return entity

    def get_all(self):
        return self.session.query(StudentExam).all()

    def get_by_id(self, id):
        return self.session.get(StudentExam, id)

    def get_full_exam_for_student(self, student_id, exam_id):
        return (
            self.session.query(StudentExam)
            .filter(
                StudentExam.student_id == student_id,
                StudentExam.exam_id == exam_id
            )
            .first()
        )

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj