from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.teacher_dto import TeacherDTO
from server.services.teacher_service import TeacherService
from server.repositories.teacher_repository import TeacherRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = TeacherRepository(session)
service = TeacherService(repo)

teachers_blueprint = Blueprint('teachers', __name__)

@teachers_blueprint.route('', methods=['POST'])
def add():
    dto = TeacherDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Teacher added'}), 201

@teachers_blueprint.route('', methods=['GET'])
def get_all():
    data = service.get_all()
    return jsonify([{
        'id': x.TeacherID,
        'firstName': x.FirstName,
        'lastName': x.LastName,
        'email': x.Email
    } for x in data])

@teachers_blueprint.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    x = service.get_by_id(id)
    return jsonify({'id': x.TeacherID})

@teachers_blueprint.route('/<int:id>', methods=['PUT'])
def update(id):
    dto = TeacherDTO(**request.get_json())
    service.update(id, dto)
    return jsonify({'message': 'Teacher updated'})

@teachers_blueprint.route('/<int:id>', methods=['DELETE'])
def delete(id):
    service.delete(id)
    return jsonify({'message': 'Teacher deleted'})