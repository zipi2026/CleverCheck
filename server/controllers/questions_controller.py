from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.question_dto import QuestionDTO
from server.services.question_service import QuestionService
from server.repositories.question_repository import QuestionRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = QuestionRepository(session)
service = QuestionService(repo)

questions_blueprint = Blueprint('questions', __name__)

@questions_blueprint.route('', methods=['POST'])
def add():
    dto = QuestionDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Question added'}), 201

@questions_blueprint.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    x = service.get_by_id(id)
    return jsonify({'id': x.QuestionID})

@questions_blueprint.route('/<int:id>', methods=['PUT'])
def update(id):
    dto = QuestionDTO(**request.get_json())
    service.update(id, dto)
    return jsonify({'message': 'Question updated'})

@questions_blueprint.route('/<int:id>', methods=['DELETE'])
def delete(id):
    service.delete(id)
    return jsonify({'message': 'Question deleted'})