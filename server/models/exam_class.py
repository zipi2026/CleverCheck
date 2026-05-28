from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from server.db.base import Base

class ExamClass(Base):
    __tablename__ = "ExamClasses"

    exam_id = Column("ExamID", Integer, ForeignKey("Exams.ExamID"), primary_key=True)
    class_id = Column("ClassID", Integer, ForeignKey("Classes.ClassID"), primary_key=True)

    exam = relationship("Exam", back_populates="exam_classes")

    class_ = relationship("Class", back_populates="exam_classes")