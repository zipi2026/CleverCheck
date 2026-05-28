from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#Base = declarative_base()
from server.db.base import Base

class Class(Base):
    """כיתה במערכת."""

    __tablename__ = "Classes"

    # =========================
    # PK
    # =========================
    id = Column("ClassID", Integer, primary_key=True, autoincrement=True)

    # =========================
    # FIELDS
    # =========================
    class_name = Column("ClassName", String(50), nullable=False, unique=True)

    # =========================
    # RELATIONSHIPS
    # =========================
    students = relationship(
        "Student",
        back_populates="class_"
    )
    exam_classes = relationship("ExamClass", back_populates="class_")
    teacher_classes = relationship("TeacherClass", back_populates="class_")


    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return f"<Class id={self.id} name={self.class_name}>"