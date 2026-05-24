from flask import Blueprint, request, jsonify
from server.dtos.student_dto import StudentDTO
from server.services.student_service import StudentService
from server.repositories.student_repository import StudentRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.students import Base

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = StudentRepository(session)

service = StudentService(repo)

students_blueprint = Blueprint('students', __name__)

@students_blueprint.route('', methods=['POST'])
def add_student():
    dto = StudentDTO(**request.get_json())
    service.add_student(dto)
    return jsonify({'message': 'Student added'}), 201

@students_blueprint.route('', methods=['GET'])
def get_students():
    data = service.get_all_students()
    return jsonify([{'id': x.StudentID, 'firstName': x.FirstName, 'lastName': x.LastName} for x in data])

@students_blueprint.route('/<int:student_id>', methods=['GET'])
def get_student(student_id):
    x = service.get_student_by_id(student_id)
    return jsonify({'id': x.StudentID})

@students_blueprint.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    dto = StudentDTO(**request.get_json())
    service.update_student(student_id, dto)
    return jsonify({'message': 'Student updated'})

@students_blueprint.route('/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    service.delete_student(student_id)
    return jsonify({'message': 'Student deleted'})
