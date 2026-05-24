
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.student_exam_dto import StudentExamDTO
from server.services.student_exam_service import StudentExamService
from server.repositories.student_exam_repository import StudentExamRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = StudentExamRepository(session)
service = StudentExamService(repo)

student_exams_blueprint = Blueprint('student_exams', __name__)

@student_exams_blueprint.route('', methods=['POST'])
def add():
    dto = StudentExamDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'StudentExam added'}), 201