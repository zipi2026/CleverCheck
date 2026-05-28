from flask import Blueprint, request, jsonify
from server.dtos.question_types_dto import QuestionTypeDTO
from server.services.question_type_service import QuestionTypeService
from server.repositories.question_type_repository import QuestionTypeRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.question_types import Base

engine = create_engine(
    'mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

repo = QuestionTypeRepository(session)
service = QuestionTypeService(repo)

question_types_blueprint = Blueprint('question_types', __name__)


@question_types_blueprint.route('', methods=['POST'])
def add_question_type():
    dto = QuestionTypeDTO(**request.get_json())
    service.add_question_type(dto)
    return jsonify({'message': 'QuestionType added'}), 201


@question_types_blueprint.route('', methods=['GET'])
def get_question_types():
    data = service.get_all_question_types()
    return jsonify([
        {
            'id': x.id,
            'typeName': x.type_name
        }
        for x in data
    ])


@question_types_blueprint.route('/<int:type_id>', methods=['GET'])
def get_question_type(type_id):
    x = service.get_question_type_by_id(type_id)
    return jsonify({
        'id': x.id,
        'typeName': x.type_name
    })


@question_types_blueprint.route('/<int:type_id>', methods=['PUT'])
def update_question_type(type_id):
    dto = QuestionTypeDTO(**request.get_json())
    service.update_question_type(type_id, dto)
    return jsonify({'message': 'QuestionType updated'})


@question_types_blueprint.route('/<int:type_id>', methods=['DELETE'])
def delete_question_type(type_id):
    service.delete_question_type(type_id)
    return jsonify({'message': 'QuestionType deleted'})