from server.models.subject import Subject
from server.exceptions.exceptions import CleverCheckBaseError

class SubjectService:
    def __init__(self, repo):
        self.repo = repo

    def add_subject(self, dto):
        if not dto.SubjectName:
            raise CleverCheckBaseError("SubjectName is required")

        self.repo.add(Subject(SubjectName=dto.SubjectName))

    def get_all_subjects(self):
        return self.repo.get_all()

    def get_subject_by_id(self, subject_id):
        subject = self.repo.get_by_id(subject_id)
        if not subject:
            raise CleverCheckBaseError(subject_id)
        return subject

    def update_subject(self, subject_id, dto):
        subject = self.repo.get_by_id(subject_id)
        if not subject:
            raise CleverCheckBaseError(subject_id)

        subject.SubjectName = dto.SubjectName
        return self.repo.update(subject_id, subject)

    def delete_subject(self, subject_id):
        subject = self.repo.delete(subject_id)
        if not subject:
            raise CleverCheckBaseError(subject_id)
        return subject