from flask import Blueprint, request, jsonify
from server.dtos.teacher_answer_dto import TeacherAnswerDTO
from server.services.teacher_answer_service import TeacherAnswerService
from server.repositories.teacher_answer_repository import TeacherAnswerRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.teacher_answer import Base

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = TeacherAnswerRepository(session)
service = TeacherAnswerService(repo)

teacher_answers_blueprint = Blueprint('teacher_answers', __name__)

@teacher_answers_blueprint.route('', methods=['POST'])
def add_teacher_answer():
    dto = TeacherAnswerDTO(**request.get_json())
    service.add_teacher_answer(dto)
    return jsonify({'message': 'TeacherAnswer added'}), 201

@teacher_answers_blueprint.route('', methods=['GET'])
def get_teacher_answers():
    data = service.get_all_teacher_answers()
    return jsonify([{'id': x.TeacherAnswerID} for x in data])

@teacher_answers_blueprint.route('/<int:teacher_answer_id>', methods=['GET'])
def get_teacher_answer(teacher_answer_id):
    x = service.get_teacher_answer_by_id(teacher_answer_id)
    return jsonify({'id': x.TeacherAnswerID})

@teacher_answers_blueprint.route('/<int:teacher_answer_id>', methods=['PUT'])
def update_teacher_answer(teacher_answer_id):
    dto = TeacherAnswerDTO(**request.get_json())
    service.update_teacher_answer(teacher_answer_id, dto)
    return jsonify({'message': 'TeacherAnswer updated'})

@teacher_answers_blueprint.route('/<int:teacher_answer_id>', methods=['DELETE'])
def delete_teacher_answer(teacher_answer_id):
    service.delete_teacher_answer(teacher_answer_id)
    return jsonify({'message': 'TeacherAnswer deleted'})