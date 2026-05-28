from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from server.db.base import Base


class TeacherClass(Base):
    __tablename__ = "TeacherClasses"

    teacher_id = Column("TeacherID", Integer, ForeignKey("Teachers.TeacherID"), primary_key=True)
    class_id = Column("ClassID", Integer, ForeignKey("Classes.ClassID"), primary_key=True)

    teacher = relationship("Teacher", back_populates="teacher_classes")

    class_ = relationship("Class", back_populates="teacher_classes")