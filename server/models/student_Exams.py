from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StudentExam(Base):
    """רישום תלמיד למבחן + תוצאות כלליות."""

    __tablename__ = "StudentExams"

    # =========================
    # PK
    # =========================
    id = Column("StudentExamID", Integer, primary_key=True, autoincrement=True)

    # =========================
    # FK
    # =========================
    exam_id = Column(
        "ExamID",
        Integer,
        ForeignKey("Exams.ExamID", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    student_id = Column(
        "StudentID",
        Integer,
        ForeignKey("Students.StudentID", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # =========================
    # TIME FIELDS
    # =========================
    start_time = Column("StartTime", DateTime, nullable=True)
    end_time = Column("EndTime", DateTime, nullable=True)

    # =========================
    # FINAL SCORE (exam level)
    # =========================
    score = Column("Score", Float, nullable=True)

    # =========================
    # CONSTRAINTS
    # =========================
    __table_args__ = (
        UniqueConstraint("ExamID", "StudentID", name="UQ_StudentExam"),
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    exam = relationship("Exam", back_populates="student_exams")
    student = relationship("Student", back_populates="student_exams")

    answers = relationship(
        "StudentAnswer",
        back_populates="student_exam",
        cascade="all, delete-orphan"
    )

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<StudentExam id={self.id} "
            f"exam_id={self.exam_id} "
            f"student_id={self.student_id} "
            f"score={self.score}>"
        )