from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.class_dto import ClassDTO
from server.services.class_service import ClassService
from server.repositories.class_repository import ClassRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = ClassRepository(session)
service = ClassService(repo)

classes_blueprint = Blueprint('classes', __name__)

@classes_blueprint.route('', methods=['POST'])
def add():
    dto = ClassDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Class added'}), 201

@classes_blueprint.route('', methods=['GET'])
def get_all():
    data = service.get_all()
    return jsonify([{'id': x.ClassID, 'name': x.ClassName} for x in data])

@classes_blueprint.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    x = service.get_by_id(id)
    return jsonify({'id': x.ClassID, 'name': x.ClassName})

@classes_blueprint.route('/<int:id>', methods=['PUT'])
def update(id):
    dto = ClassDTO(**request.get_json())
    service.update(id, dto)
    return jsonify({'message': 'Class updated'})

@classes_blueprint.route('/<int:id>', methods=['DELETE'])
def delete(id):
    service.delete(id)
    return jsonify({'message': 'Class deleted'})