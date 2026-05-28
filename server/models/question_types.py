from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from server.db.base import Base

#Base = declarative_base()

class QuestionType(Base):
    """סוג שאלה (למשל: פתוחה / אמריקאית)."""

    __tablename__ = "QuestionTypes"

    # =========================
    # PK
    # =========================
    id = Column("QuestionTypeID", Integer, primary_key=True, autoincrement=True)

    # =========================
    # FIELDS
    # =========================
    type_name = Column("TypeName", String(50), nullable=False, unique=True)

    # =========================
    # RELATIONSHIPS
    # =========================
    questions = relationship(
        "Question",
        back_populates="question_type"
    )

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return f"<QuestionType id={self.id} name={self.type_name}>"