from flask import Blueprint, request, jsonify
from server.dtos.exam_dto import ExamDTO
from server.services.exam_service import ExamService
from server.repositories.exam_repository import ExamRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.exams import Base

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = ExamRepository(session)
service = ExamService(repo)

exams_blueprint = Blueprint('exams', __name__)

@exams_blueprint.route('', methods=['POST'])
def add_exam():
    dto = ExamDTO(**request.get_json())
    service.add_exam(dto)
    return jsonify({'message': 'Exam added'}), 201

@exams_blueprint.route('', methods=['GET'])
def get_exams():
    data = service.get_all_exams()
    return jsonify([{'id': x.ExamID, 'name': x.ExamName} for x in data])

@exams_blueprint.route('/<int:exam_id>', methods=['GET'])
def get_exam(exam_id):
    x = service.get_exam_by_id(exam_id)
    return jsonify({'id': x.ExamID})

@exams_blueprint.route('/<int:exam_id>', methods=['PUT'])
def update_exam(exam_id):
    dto = ExamDTO(**request.get_json())
    service.update_exam(exam_id, dto)
    return jsonify({'message': 'Exam updated'})

@exams_blueprint.route('/<int:exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    service.delete_exam(exam_id)
    return jsonify({'message': 'Exam deleted'})