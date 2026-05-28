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
        return self.session.get(Student, id)

    def update(self, id, new_data: Student):
        obj = self.get_by_id(id)

        if not obj:
            return None

        obj.first_name = new_data.first_name
        obj.last_name = new_data.last_name
        obj.class_id = new_data.class_id
        obj.is_active = new_data.is_active
        obj.password_hash = new_data.password_hash

        self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj