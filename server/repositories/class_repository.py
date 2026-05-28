from server.models.classes import Class
from sqlalchemy.orm import Session


class ClassRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: Class):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(Class).all()

    def get_by_id(self, id):
        return self.session.get(Class, id)

    def update(self, id, new_data: Class):
        obj = self.get_by_id(id)

        if not obj:
            return None

        obj.class_name = new_data.class_name
        self.session.commit()

        return obj

    def delete(self, id):
        obj = self.get_by_id(id)

        if obj:
            self.session.delete(obj)
            self.session.commit()

        return obj

    def exists_by_name(self, name):
        return (
            self.session.query(Class)
            .filter_by(class_name=name)
            .first()
            is not None
        )