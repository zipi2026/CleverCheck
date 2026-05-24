from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.exam_dto import ExamDTO
from server.services.exam_service import ExamService
from server.repositories.exam_repository import ExamRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = ExamRepository(session)
service = ExamService(repo)

exams_blueprint = Blueprint('exams', __name__)

@exams_blueprint.route('', methods=['POST'])
def add():
    dto = ExamDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Exam added'}), 201

@exams_blueprint.route('', methods=['GET'])
def get_all():
    data = service.get_all()
    return jsonify([{'id': x.ExamID, 'name': x.ExamName} for x in data])

@exams_blueprint.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    x = service.get_by_id(id)
    return jsonify({'id': x.ExamID})

@exams_blueprint.route('/<int:id>', methods=['PUT'])
def update(id):
    dto = ExamDTO(**request.get_json())
    service.update(id, dto)
    return jsonify({'message': 'Exam updated'})

@exams_blueprint.route('/<int:id>', methods=['DELETE'])
def delete(id):
    service.delete(id)
    return jsonify({'message': 'Exam deleted'})