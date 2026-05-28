from server.models.classes import Class
from server.exceptions.exceptions import CleverCheckBaseError


class ClassService:
    def __init__(self, repo):
        self.repo = repo

    def add_class(self, dto):
        self.repo.add(
            Class(
                class_name=dto.class_name
            )
        )

    def get_all_classes(self):
        return self.repo.get_all()

    def get_class_by_id(self, class_id):
        obj = self.repo.get_by_id(class_id)
        if not obj:
            raise CleverCheckBaseError(class_id)
        return obj

    def update_class(self, class_id, dto):
        obj = self.repo.update(
            class_id,
            Class(
                class_name=dto.class_name
            )
        )

        if not obj:
            raise CleverCheckBaseError(class_id)

        return obj

    def delete_class(self, class_id):
        obj = self.repo.delete(class_id)
        if not obj:
            raise CleverCheckBaseError(class_id)
        return obj