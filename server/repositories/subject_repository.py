from server.models.subject import Subject
from sqlalchemy.orm import Session

class SubjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: Subject):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_all(self):
        return self.session.query(Subject).all()

    def get_by_id(self, id):
        return self.session.query(Subject).get(id)

    def update(self, id, new_data: Subject):
        obj = self.get_by_id(id)
        if obj:
            obj.SubjectName = new_data.SubjectName
            self.session.commit()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj

    def exists_by_name(self, name):
        return self.session.query(Subject).filter_by(SubjectName=name).first() is not None