from flask import Blueprint, request, jsonify
from server.dtos.class_dto import ClassDTO
from server.services.class_service import ClassService
from server.repositories.class_repository import ClassRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.classes import Base

engine = create_engine(
    'mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

repo = ClassRepository(session)
service = ClassService(repo)

classes_blueprint = Blueprint('classes', __name__)


@classes_blueprint.route('', methods=['POST'])
def add_class():
    dto = ClassDTO(**request.get_json())
    service.add_class(dto)
    return jsonify({'message': 'Class added'}), 201


@classes_blueprint.route('', methods=['GET'])
def get_classes():
    data = service.get_all_classes()
    return jsonify([
        {
            'id': c.id,
            'className': c.class_name
        }
        for c in data
    ])


@classes_blueprint.route('/<int:class_id>', methods=['GET'])
def get_class(class_id):
    c = service.get_class_by_id(class_id)
    return jsonify({
        'id': c.id,
        'className': c.class_name
    })


@classes_blueprint.route('/<int:class_id>', methods=['PUT'])
def update_class(class_id):
    dto = ClassDTO(**request.get_json())
    service.update_class(class_id, dto)
    return jsonify({'message': 'Class updated'})


@classes_blueprint.route('/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    service.delete_class(class_id)
    return jsonify({'message': 'Class deleted'})