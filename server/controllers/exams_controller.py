from datetime import datetime

from flask import Blueprint, request, jsonify


from server.dtos.exams_dto import ExamDTO
from server.services.exam_service import ExamService
from server.repositories.exam_repository import ExamRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models.exams import Base
from server.services.jwt_service import get_student_data

engine = create_engine(
    'mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

repo = ExamRepository(session)
service = ExamService(repo)

exams_blueprint = Blueprint('exams', __name__)


@exams_blueprint.route('', methods=['POST'])
def add_exam():
    dto = ExamDTO(**request.get_json())
    service.add_exam(dto)
    return jsonify({'message': 'Exam added'}), 201


@exams_blueprint.route('', methods=['GET'])
def get_exams():
    data = service.get_all_exams()
    return jsonify([
        {
            'id': e.id,
            'examName': e.exam_name,
            'teacherID': e.teacher_id,
            'subjectID': e.subject_id,
            'startTime': e.start_time,
            'endTime': e.end_time,
            'durationMinutes': e.duration_minutes,
            'status': e.status
        }
        for e in data
    ])


@exams_blueprint.route('/<int:exam_id>', methods=['GET'])
def get_student_exam(exam_id):
    student_id = get_student_data().get('student_id')

    if not student_id:
        return jsonify({"error": "Unauthorized"}), 401

    exam = service.get_exam_by_id(exam_id)
    questions = service.get_questions(exam_id)

    student_exam = service.get_or_create_student_exam(student_id, exam_id)

    answers = service.get_answers(student_exam.id)

    return jsonify({
        "exam": {
            "id": exam.id,
            "examName": exam.exam_name,
            "subjectID": exam.subject_id,
            "status": exam.status,
            "durationMinutes": exam.duration_minutes,
            "startTime": exam.start_time,
            "endTime": exam.end_time
        },
        "studentExam": {
            "studentExamId": student_exam.id,
            "endTime": student_exam.end_time
        },
        "serverTime": datetime.utcnow().isoformat(),
        "questions": questions,
        "answers": answers
    })

@exams_blueprint.route('/<int:exam_id>', methods=['PUT'])
def update_exam(exam_id):
    dto = ExamDTO(**request.get_json())
    service.update_exam(exam_id, dto)
    return jsonify({'message': 'Exam updated'})


@exams_blueprint.route('/<int:exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    service.delete_exam(exam_id)
    return jsonify({'message': 'Exam deleted'})