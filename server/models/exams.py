from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Exam(Base):
    """מבחן שנוצר על ידי מורה."""

    __tablename__ = "Exams"

    # =========================
    # PK
    # =========================
    id = Column("ExamID", Integer, primary_key=True, autoincrement=True)

    # =========================
    # FIELDS
    # =========================
    exam_name = Column("ExamName", String(100), nullable=False)

    teacher_id = Column(
        "TeacherID",
        Integer,
        ForeignKey("Teachers.TeacherID"),
        nullable=False,
        index=True
    )

    subject_id = Column(
        "SubjectID",
        Integer,
        ForeignKey("Subjects.SubjectID"),
        nullable=False,
        index=True
    )

    start_time = Column("StartTime", DateTime, nullable=False)
    end_time = Column("EndTime", DateTime, nullable=False)

    duration_minutes = Column("DurationMinutes", Integer, nullable=False)

    created_at = Column("CreatedAt", DateTime, default=datetime.utcnow)

    status = Column(
        "Status",
        String(20),
        nullable=False,
        default="Draft"
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    teacher = relationship("Teacher")
    subject = relationship("Subject")

    questions = relationship(
        "Question",
        back_populates="exam",
        cascade="all, delete-orphan"
    )

    student_exams = relationship(
        "StudentExam",
        back_populates="exam",
        cascade="all, delete-orphan"
    )

    exam_classes = relationship(
        "ExamClass",
        back_populates="exam",
        cascade="all, delete-orphan"
    )

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<Exam id={self.id} "
            f"name={self.exam_name} "
            f"status={self.status}>"
        )