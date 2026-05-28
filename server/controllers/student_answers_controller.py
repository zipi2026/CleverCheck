from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.student_answer import Base
from server.dtos.student_answer_dto import StudentAnswerDTO
from server.repositories.student_answer_repository import StudentAnswerRepository
from server.services.student_answer_service import StudentAnswerService

engine = create_engine(
    'mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = StudentAnswerRepository(session)
service = StudentAnswerService(repo)

student_answers_blueprint = Blueprint('student_answers', __name__)

@student_answers_blueprint.route('', methods=['POST'])
def add_student_answer():
    dto = StudentAnswerDTO(**request.get_json())
    service.add_student_answer(dto)
    return jsonify({'message': 'StudentAnswer added'}), 201


@student_answers_blueprint.route('', methods=['GET'])
def get_all_student_answers():
    data = service.get_all_student_answers()
    return jsonify([{'id': x.id, 'score': x.score} for x in data])


@student_answers_blueprint.route('/<int:answer_id>', methods=['GET'])
def get_student_answer(answer_id):
    x = service.get_student_answer_by_id(answer_id)
    return jsonify({'id': x.id, 'score': x.score})


@student_answers_blueprint.route('/<int:answer_id>', methods=['PUT'])
def update_student_answer(answer_id):
    dto = StudentAnswerDTO(**request.get_json())
    service.update_student_answer(answer_id, dto)
    return jsonify({'message': 'StudentAnswer updated'})


@student_answers_blueprint.route('/<int:answer_id>', methods=['DELETE'])
def delete_student_answer(answer_id):
    service.delete_student_answer(answer_id)
    return jsonify({'message': 'StudentAnswer deleted'})