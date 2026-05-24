from sqlalchemy import (
    Column, Integer, String,
    Boolean, ForeignKey
)
from sqlalchemy.orm import relationship

from models.base import Base


class Student(Base):
    """סטודנט במערכת."""

    __tablename__ = "Students"

    # =========================
    # PK
    # =========================
    id = Column("StudentID", Integer, primary_key=True)

    # =========================
    # FIELDS
    # =========================
    password_hash = Column("PasswordHash", String(255), nullable=False)

    first_name = Column("FirstName", String(100), nullable=False)
    last_name = Column("LastName", String(100), nullable=False)

    class_id = Column(
        "ClassID",
        Integer,
        ForeignKey("Classes.ClassID"),
        nullable=False,
        index=True
    )

    is_active = Column("IsActive", Boolean, default=False)

    # =========================
    # RELATIONSHIPS
    # =========================
    class_ = relationship("Class", back_populates="students")

    student_exams = relationship(
        "StudentExam",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<Student id={self.id} "
            f"name={self.first_name} {self.last_name}>"
        )