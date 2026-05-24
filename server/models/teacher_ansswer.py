from sqlalchemy import (
    Column, Integer, Text,
    ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship

from models.base import Base


class TeacherAnswer(Base):
    """תשובת מורה לשאלה (פתוחה או אמריקאית נכונה)."""

    __tablename__ = "TeacherAnswers"

    # =========================
    # PK
    # =========================
    id = Column("TeacherAnswerID", Integer, primary_key=True, autoincrement=True)

    # =========================
    # FK
    # =========================
    question_id = Column(
        "QuestionID",
        Integer,
        ForeignKey("Questions.QuestionID", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    correct_option_id = Column(
        "CorrectOptionID",
        Integer,
        ForeignKey("Options.OptionID"),
        nullable=True
    )

    # =========================
    # ANSWER DATA
    # =========================
    answer_text = Column("AnswerText", Text, nullable=True)

    # =========================
    # CONSTRAINT (only one type)
    # =========================
    __table_args__ = (
        CheckConstraint(
            """
            (AnswerText IS NOT NULL AND CorrectOptionID IS NULL)
            OR
            (AnswerText IS NULL AND CorrectOptionID IS NOT NULL)
            """,
            name="CK_TeacherAnswers_Type"
        ),
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    question = relationship("Question", back_populates="teacher_answer")
    correct_option = relationship("Option")

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<TeacherAnswer id={self.id} "
            f"question_id={self.question_id}>"
        )