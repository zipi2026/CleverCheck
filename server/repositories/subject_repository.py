from sqlalchemy.orm import Session

class SubjectRepository:
    def __init__(self, session: Session):
        self.session = session
