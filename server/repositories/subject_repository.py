# repository/subject_repository.py
from server.models.subject import Subject
from sqlalchemy.orm import Session

class SubjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, subject: Subject):
        self.session.add(subject)
        self.session.commit()
        return subject

    def get_all(self):
        return self.session.query(Subject).all()

    def get_by_id(self, subject_id):
        return self.session.query(Subject).get(subject_id)

    def update(self, subject_id, new_data: Subject):
        subject = self.get_by_id(subject_id)
        if subject:
            subject.SubjectName = new_data.SubjectName
            self.session.commit()
        return subject

    def delete(self, subject_id):
        subject = self.get_by_id(subject_id)
        if subject:
            self.session.delete(subject)
            self.session.commit()
        return subject

    def exists_by_name(self, name):
        return self.session.query(Subject).filter_by(SubjectName=name).first() is not None