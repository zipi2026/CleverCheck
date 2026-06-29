from urllib import request

from fontTools.config import OPTIONS

from server.services.auth_service import validate_student
from server.services.jwt_service import create_token
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
        if request.method == 'OPTIONS':
            return '',200
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "נדרש JSON"}), 400

        student_name = data.get("student_name")
        password = data.get("password")

        try:
            student = validate_student(session, student_name, password)

            if not student:
                return jsonify({"error": "שם משתמש או סיסמה שגויים"}), 401

            token = create_token(student)

            response = jsonify({"message": "login success"})

            response.set_cookie(
                "token",
                token,
                httponly=True,
                samesite="Lax",
                secure=False,
                path="/"
            )
                # בפרודקשן True


            return response, 200

        except Exception as e:
            print("LOGIN ERROR:", e)
            return jsonify({"error": str(e)}), 500
@auth_bp.route('/me', methods=['GET'])
def get_student_me():
    try:
        from server.services.jwt_service import get_student_data
        data = get_student_data()
        print(data)
        return jsonify({
            'student_id': data['student_id'],
            'role': data['role'],
            'student_name': data.get('student_name', 'student'),
        }), 200
    except Exception:
        return jsonify({'error': 'טוקן לא תקין'}), 401

