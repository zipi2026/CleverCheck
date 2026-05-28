from server.models.teachers import Teacher
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
            obj.first_name = new_data.first_name
            obj.last_name = new_data.last_name
            obj.email = new_data.email
            obj.password_hash = new_data.password_hash
            obj.is_active = new_data.is_active
            obj.role = new_data.role
            self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj

    def exists_by_email(self, email):
        return self.session.query(Teacher).filter_by(email=email).first() is not None