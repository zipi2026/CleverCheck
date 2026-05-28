from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.dtos.subject_dto import SubjectDTO
from server.services.subject_service import SubjectService
from server.repositories.subject_repository import SubjectRepository
from server.models.subject import Base


engine = create_engine(
    'mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

repo = SubjectRepository(session)
service = SubjectService(repo)

subject_blueprint = Blueprint('subjects', __name__)


@subject_blueprint.route('', methods=['POST'])
def add_subject():
    dto = SubjectDTO(**request.get_json())
    service.add_subject(dto)
    return jsonify({'message': 'Subject added'}), 201


@subject_blueprint.route('', methods=['GET'])
def get_subjects():
    subjects = service.get_all_subjects()
    return jsonify([
        {
            'id': s.id,
            'subject_name': s.subject_name
        } for s in subjects
    ])


@subject_blueprint.route('/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    subject = service.get_subject_by_id(subject_id)
    return jsonify({
        'id': subject.id,
        'subject_name': subject.subject_name
    })


@subject_blueprint.route('/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    dto = SubjectDTO(**request.get_json())
    service.update_subject(subject_id, dto)
    return jsonify({'message': 'Subject updated'})


@subject_blueprint.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    service.delete_subject(subject_id)
    return jsonify({'message': 'Subject deleted'})