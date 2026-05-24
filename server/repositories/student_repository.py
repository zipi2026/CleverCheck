from server.models.student import Student
from sqlalchemy.orm import Session

class StudentRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: Student):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(Student).all()

    def get_by_id(self, id):
        return self.session.query(Student).get(id)

    def update(self, id, new_data: Student):
        obj = self.get_by_id(id)
        if obj:
            obj.FirstName = new_data.FirstName
            obj.LastName = new_data.LastName
            obj.ClassID = new_data.ClassID
            obj.IsActive = new_data.IsActive
            self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj