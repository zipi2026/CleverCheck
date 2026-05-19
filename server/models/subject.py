from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Subject(Base):
    __tablename__ = 'subjects'
    SubjectID = Column(Integer, primary_key=True)
    SubjectName = Column(String(50), unique=True, nullable=False)