from sqlalchemy import (
    Column, Integer, String,
    Boolean
)
from sqlalchemy.orm import relationship

from models.base import Base


class Teacher(Base):
    """מורה במערכת."""

    __tablename__ = "Teachers"

    # =========================
    # PK
    # =========================
    id = Column("TeacherID", Integer, primary_key=True)

    # =========================
    # FIELDS
    # =========================
    password_hash = Column("PasswordHash", String(255), nullable=False)

    first_name = Column("FirstName", String(50), nullable=False)
    last_name = Column("LastName", String(50), nullable=False)

    email = Column("Email", String(100), nullable=False, unique=True)

    is_active = Column("IsActive", Boolean, default=False)

    role = Column("Role", String(10), default="teacher")

    # =========================
    # RELATIONSHIPS
    # =========================
    exams = relationship(
        "Exam",
        back_populates="teacher"
    )

    # אם משתמשים ב־TeacherClasses
    teacher_classes = relationship(
        "TeacherClass",
        back_populates="teacher",
        cascade="all, delete-orphan"
    )

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<Teacher id={self.id} "
            f"name={self.first_name} {self.last_name}>"
        )