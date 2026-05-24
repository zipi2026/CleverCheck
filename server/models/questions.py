from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Question(Base):
    """שאלה בתוך מבחן."""

    __tablename__ = "Questions"

    # =========================
    # PK
    # =========================
    id = Column("QuestionID", Integer, primary_key=True, autoincrement=True)

    # =========================
    # FIELDS
    # =========================
    question_number = Column("QuestionNumber", Integer, nullable=False)

    exam_id = Column(
        "ExamID",
        Integer,
        ForeignKey("Exams.ExamID", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    question_text = Column("QuestionText", Text, nullable=False)

    question_type_id = Column(
        "QuestionTypeID",
        Integer,
        ForeignKey("QuestionTypes.QuestionTypeID"),
        nullable=False,
        index=True
    )

    max_score = Column("MaxScore", Float, nullable=False)

    # =========================
    # CONSTRAINTS
    # =========================
    __table_args__ = (
        UniqueConstraint(
            "ExamID",
            "QuestionNumber",
            name="UQ_Exam_QuestionNumber"
        ),
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    exam = relationship("Exam", back_populates="questions")
    question_type = relationship("QuestionType")

    options = relationship(
        "Option",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    teacher_answer = relationship(
        "TeacherAnswer",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan"
    )

    student_answers = relationship(
        "StudentAnswer",
        back_populates="question"
    )

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<Question id={self.id} "
            f"exam_id={self.exam_id} "
            f"number={self.question_number}>"
        )