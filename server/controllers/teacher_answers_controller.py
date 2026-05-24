
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.teacher_answer_dto import TeacherAnswerDTO
from server.services.teacher_answer_service import TeacherAnswerService
from server.repositories.teacher_answer_repository import TeacherAnswerRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = TeacherAnswerRepository(session)
service = TeacherAnswerService(repo)

teacher_answers_blueprint = Blueprint('teacher_answers', __name__)

@teacher_answers_blueprint.route('', methods=['POST'])
def add():
    dto = TeacherAnswerDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Added'}), 201
