from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.question_type_dto import QuestionTypeDTO
from server.services.question_type_service import QuestionTypeService
from server.repositories.question_type_repository import QuestionTypeRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = QuestionTypeRepository(session)
service = QuestionTypeService(repo)

question_types_blueprint = Blueprint('question_types', __name__)

@question_types_blueprint.route('', methods=['POST'])
def add():
    dto = QuestionTypeDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Added'}), 201

@question_types_blueprint.route('', methods=['GET'])
def get_all():
    data = service.get_all()
    return jsonify([{'id': x.QuestionTypeID, 'name': x.TypeName} for x in data])