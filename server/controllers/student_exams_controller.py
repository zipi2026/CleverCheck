from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.dtos.student_exam_dto import StudentExamDTO
from server.exceptions.exceptions import CleverCheckBaseError
from server.services.jwt_service import get_student_data
from server.services.student_exam_service import StudentExamService
from server.repositories.student_exam_repository import StudentExamRepository
from server.models.student_exams import Base

engine = create_engine(
    'mssql+pyodbc://localhost/CleverCheckDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

repo = StudentExamRepository(session)
service = StudentExamService(repo)

student_exams_blueprint = Blueprint('student_exams', __name__)


@student_exams_blueprint.route('', methods=['POST'])
def add_student_exam():
    dto = StudentExamDTO(**request.get_json())
    service.add_student_exam(dto)
    return jsonify({'message': 'StudentExam added'}), 201


@student_exams_blueprint.route('', methods=['GET'])
def get_student_exams():
    data = service.get_all_student_exams()
    return jsonify([
        {
            'id': x.id,
            'score': x.score
        } for x in data
    ])


@student_exams_blueprint.route('/<int:student_exam_id>', methods=['PUT'])
def update_student_exam(student_exam_id):
    dto = StudentExamDTO(**request.get_json())
    service.update_student_exam(student_exam_id, dto)
    return jsonify({'message': 'StudentExam updated'})


@student_exams_blueprint.route('/<int:student_exam_id>', methods=['DELETE'])
def delete_student_exam(student_exam_id):
    service.delete_student_exam(student_exam_id)
    return jsonify({'message': 'StudentExam deleted'})


@student_exams_blueprint.route('/<int:student_exam_id>/finish', methods=['POST'])
def finish_exam(student_exam_id):
    return service.update_exam_grades(student_exam_id)


@student_exams_blueprint.route('/exam/<int:exam_id>', methods=['GET'])
def get_student_exam(exam_id):
    data = get_student_data()
    if not data:
        return jsonify({'message': 'StudentExam not found'}), 404
    student_id = data.get('student_id')

    if not student_id:
        return jsonify({"error": "Unauthorized"}), 401

    student_exam = service.get_full_exam(student_id, exam_id)
    exam = student_exam.exam

    return jsonify({
        "exam": {
            "id": exam.id,
            "name": exam.exam_name,
            "status": exam.status,
            "durationMinutes": exam.duration_minutes,
            "startTime": exam.start_time,
            "endTime": exam.end_time,
        },

        "studentExam": {
            "id": student_exam.id,
            "score": student_exam.score
        },

        "questions": [
            {
                "id": q.id,
                "text": q.question_text,
                "typeId": q.question_type_id,
                "maxScore": q.max_score,

                "options": [
                    {
                        "id": o.id,
                        "text": o.option_text
                    }
                    for o in q.options
                ] if q.question_type_id == 1 else []
            }
            for q in exam.questions
        ],

        "answers": [
            {
                "questionId": a.question_id,
                "answerText": a.answer_text,
                "selectedOptionId": a.selected_option_id,
                "score": a.score
            }
            for a in student_exam.answers
        ]
    })

@student_exams_blueprint.route('/<int:student_exam_id>/results', methods=['GET'])
def get_results(student_exam_id):
    try:
        return service.get_results(student_exam_id)
    except CleverCheckBaseError:
        return jsonify({"error": "Student exam not found"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500