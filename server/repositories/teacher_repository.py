from server.models.teacher import Teacher
from sqlalchemy.orm import Session

class TeacherRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: Teacher):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(Teacher).all()

    def get_by_id(self, id):
        return self.session.query(Teacher).get(id)

    def update(self, id, new_data: Teacher):
        obj = self.get_by_id(id)
        if obj:
            obj.FirstName = new_data.FirstName
            obj.LastName = new_data.LastName
            obj.Email = new_data.Email
            obj.IsActive = new_data.IsActive
            obj.Role = new_data.Role
            self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj

    def exists_by_email(self, email):
        return self.session.query(Teacher).filter_by(Email=email).first() is not None