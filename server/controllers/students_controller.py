from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.student_dto import StudentDTO
from server.services.student_service import StudentService
from server.repositories.student_repository import StudentRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = StudentRepository(session)
service = StudentService(repo)

students_blueprint = Blueprint('students', __name__)

@students_blueprint.route('', methods=['POST'])
def add():
    dto = StudentDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Student added'}), 201

@students_blueprint.route('', methods=['GET'])
def get_all():
    data = service.get_all()
    return jsonify([{'id': x.StudentID, 'firstName': x.FirstName, 'lastName': x.LastName} for x in data])

@students_blueprint.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    x = service.get_by_id(id)
    return jsonify({'id': x.StudentID})

@students_blueprint.route('/<int:id>', methods=['PUT'])
def update(id):
    dto = StudentDTO(**request.get_json())
    service.update(id, dto)
    return jsonify({'message': 'Student updated'})

@students_blueprint.route('/<int:id>', methods=['DELETE'])
def delete(id):
    service.delete(id)
    return jsonify({'message': 'Student deleted'})