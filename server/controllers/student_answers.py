from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.student_answer_dto import StudentAnswerDTO
from server.services.student_answer_service import StudentAnswerService
from server.repositories.student_answer_repository import StudentAnswerRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = StudentAnswerRepository(session)
service = StudentAnswerService(repo)

student_answers_blueprint = Blueprint('student_answers', __name__)

@student_answers_blueprint.route('', methods=['POST'])
def add():
    dto = StudentAnswerDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Answer added'}), 201
