from flask import Blueprint, request, jsonify
from server.dtos.option_dto import OptionDTO
from server.services.option_service import OptionService
from server.repositories.option_repository import OptionRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.options import Base

engine = create_engine(
    'mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

repo = OptionRepository(session)
service = OptionService(repo)

options_blueprint = Blueprint('options', __name__)


@options_blueprint.route('', methods=['POST'])
def add_option():
    dto = OptionDTO(**request.get_json())
    service.add_option(dto)
    return jsonify({'message': 'Option added'}), 201


@options_blueprint.route('', methods=['GET'])
def get_options():
    data = service.get_all_options()
    return jsonify([
        {
            'id': o.OptionID,
            'optionNumber': o.OptionNumber,
            'questionID': o.QuestionID,
            'optionText': o.OptionText
        }
        for o in data
    ])


@options_blueprint.route('/<int:option_id>', methods=['GET'])
def get_option(option_id):
    o = service.get_option_by_id(option_id)
    return jsonify({
        'id': o.OptionID,
        'optionNumber': o.OptionNumber,
        'questionID': o.QuestionID,
        'optionText': o.OptionText
    })


@options_blueprint.route('/<int:option_id>', methods=['PUT'])
def update_option(option_id):
    dto = OptionDTO(**request.get_json())
    service.update_option(option_id, dto)
    return jsonify({'message': 'Option updated'})


@options_blueprint.route('/<int:option_id>', methods=['DELETE'])
def delete_option(option_id):
    service.delete_option(option_id)
    return jsonify({'message': 'Option deleted'})