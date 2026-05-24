
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.base import Base
from server.dtos.option_dto import OptionDTO
from server.services.option_service import OptionService
from server.repositories.option_repository import OptionRepository

engine = create_engine('mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = OptionRepository(session)
service = OptionService(repo)

options_blueprint = Blueprint('options', __name__)

@options_blueprint.route('', methods=['POST'])
def add():
    dto = OptionDTO(**request.get_json())
    service.add(dto)
    return jsonify({'message': 'Option added'}), 201

@options_blueprint.route('/<int:id>', methods=['DELETE'])
def delete(id):
    service.delete(id)
    return jsonify({'message': 'Option deleted'})
