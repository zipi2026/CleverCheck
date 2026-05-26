from flask import Blueprint, request, jsonify
from server.dtos.student_exam_dto import StudentExamDTO
from server.services.student_exam_service import StudentExamService
from server.repositories.student_exam_repository import StudentExamRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.student_exams import Base

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = StudentExamRepository(session)
service = StudentExamService(repo)

student_exams_blueprint = Blueprint('student_exams', __name__)

@student_exams_blueprint.route('', methods=['POST'])
def add_student_exam():
    dto = StudentExamDTO(**request.get_json())
    service.add_student_exam(dto)
    return jsonify({'message': 'StudentExam added'}), 201

@student_exams_blueprint.route('', methods=['GET'])
def get_student_exams():
    data = service.get_all_student_exams()
    return jsonify([{'id': x.StudentExamID, 'score': x.Score} for x in data])

@student_exams_blueprint.route('/<int:student_exam_id>', methods=['GET'])
def get_student_exam(student_exam_id):
    x = service.get_student_exam_by_id(student_exam_id)
    return jsonify({'id': x.StudentExamID})

@student_exams_blueprint.route('/<int:student_exam_id>', methods=['PUT'])
def update_student_exam(student_exam_id):
    dto = StudentExamDTO(**request.get_json())
    service.update_student_exam(student_exam_id, dto)
    return jsonify({'message': 'StudentExam updated'})

@student_exams_blueprint.route('/<int:student_exam_id>', methods=['DELETE'])
def delete_student_exam(student_exam_id):
    service.delete_student_exam(student_exam_id)
    return jsonify({'message': 'StudentExam deleted'})