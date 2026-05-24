from sqlalchemy import (
    Column, Integer, Float, String,
    ForeignKey, Text, CheckConstraint
)
from sqlalchemy.orm import relationship

from models.base import Base


class StudentAnswer(Base):
    """תשובת תלמיד לשאלה במבחן (פתוחה או אמריקאית)."""

    __tablename__ = "StudentAnswers"

    # =========================
    # PK
    # =========================
    id = Column("AnswerID", Integer, primary_key=True, autoincrement=True)

    # =========================
    # FK
    # =========================
    student_exam_id = Column(
        "StudentExamID",
        Integer,
        ForeignKey("StudentExams.StudentExamID", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    question_id = Column(
        "QuestionID",
        Integer,
        ForeignKey("Questions.QuestionID"),
        nullable=False,
        index=True
    )

    selected_option_id = Column(
        "SelectedOptionID",
        Integer,
        ForeignKey("Options.OptionID"),
        nullable=True
    )

    # =========================
    # ANSWER DATA
    # =========================
    answer_text = Column("AnswerText", Text, nullable=True)

    score = Column(
        "Score",
        Float,
        nullable=True
    )

    # =========================
    # CONSTRAINT (only one type of answer)
    # =========================
    __table_args__ = (
        CheckConstraint(
            """
            (AnswerText IS NOT NULL AND SelectedOptionID IS NULL)
            OR
            (AnswerText IS NULL AND SelectedOptionID IS NOT NULL)
            """,
            name="CK_StudentAnswers_AnswerType"
        ),
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    student_exam = relationship("StudentExam", back_populates="answers")
    question = relationship("Question")
    option = relationship("Option")

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<StudentAnswer id={self.id} "
            f"question_id={self.question_id} "
            f"score={self.score}>"
        )