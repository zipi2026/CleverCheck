from flask import Blueprint, request, jsonify
from server.dtos.teacher_dto import TeacherDTO
from server.services.teacher_service import TeacherService
from server.repositories.teacher_repository import TeacherRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.teachers import Base

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = TeacherRepository(session)
service = TeacherService(repo)

teachers_blueprint = Blueprint('teachers', __name__)

@teachers_blueprint.route('', methods=['POST'])
def add_teacher():
    dto = TeacherDTO(**request.get_json())
    service.add_teacher(dto)
    return jsonify({'message': 'Teacher added'}), 201

@teachers_blueprint.route('', methods=['GET'])
def get_teachers():
    data = service.get_all_teachers()
    return jsonify([{'id': x.TeacherID, 'firstName': x.FirstName, 'lastName': x.LastName} for x in data])

@teachers_blueprint.route('/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    x = service.get_teacher_by_id(teacher_id)
    return jsonify({'id': x.TeacherID})

@teachers_blueprint.route('/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    dto = TeacherDTO(**request.get_json())
    service.update_teacher(teacher_id, dto)
    return jsonify({'message': 'Teacher updated'})

@teachers_blueprint.route('/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    service.delete_teacher(teacher_id)
    return jsonify({'message': 'Teacher deleted'})
