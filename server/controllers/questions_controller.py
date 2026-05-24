from flask import Blueprint, request, jsonify
from server.dtos.question_dto import QuestionDTO
from server.services.question_service import QuestionService
from server.repositories.question_repository import QuestionRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.questions import Base

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = QuestionRepository(session)
service = QuestionService(repo)

questions_blueprint = Blueprint('questions', __name__)

@questions_blueprint.route('', methods=['POST'])
def add_question():
    dto = QuestionDTO(**request.get_json())
    service.add_question(dto)
    return jsonify({'message': 'Question added'}), 201

@questions_blueprint.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    x = service.get_question_by_id(question_id)
    return jsonify({'id': x.QuestionID})

@questions_blueprint.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    dto = QuestionDTO(**request.get_json())
    service.update_question(question_id, dto)
    return jsonify({'message': 'Question updated'})

@questions_blueprint.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    service.delete_question(question_id)
    return jsonify({'message': 'Question deleted'})