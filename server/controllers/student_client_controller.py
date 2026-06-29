from flask import Blueprint, jsonify, request

student_client_bp = Blueprint('student_client', __name__)




@student_client_bp.route('/exams', methods=['GET'])
def list_student_exams():
    return jsonify([
        {
            'examId': 1,
            'name': 'מבחן מועד א – אלגברה',
            'subject': 'מתמטיקה',
            'status': 'Active',
            'durationMinutes': 45,
        },
        {
            'examId': 2,
            'name': 'מבחן היסטוריה – מסכם',
            'subject': 'היסטוריה',
            'status': 'InProgress',
            'durationMinutes': 30,
        },
    ])


@student_client_bp.route('/exams/<int:exam_id>', methods=['GET'])
def get_student_exam(exam_id: int):
    return jsonify({
        'exam': {
            'examId': exam_id,
            'name': 'מבחן מועד א – אלגברה',
            'subject': 'מתמטיקה',
            'durationMinutes': 45,
        },
        'studentExam': {
            'studentExamId': exam_id * 100,
            'status': 'Active',
            'startTime': '2025-01-01T00:00:00.000Z',
            'endTime': '2030-01-01T00:00:00.000Z',
        },
        'questions': [
            {
                'questionId': 1,
                'questionNumber': 1,
                'text': 'פתרו את המשוואה: 3x + 7 = 22',
                'type': 'TEXT',
                'maxScore': 5,
                'options': [],
            }
        ],
        'answers': [],
        'serverTime': '2025-01-01T00:00:00.000Z',
    })


@student_client_bp.route('/exams/<int:exam_id>/answers', methods=['POST'])
def save_student_answer(exam_id: int):
    payload = request.get_json(silent=True) or {}
    return jsonify({'success': True, 'examId': exam_id, 'payload': payload})


@student_client_bp.route('/exams/<int:exam_id>/submit', methods=['POST'])
def submit_student_exam(exam_id: int):
    payload = request.get_json(silent=True) or {}
    return jsonify({'success': True, 'examId': exam_id, 'payload': payload})


@student_client_bp.route('/exams/<int:exam_id>/results', methods=['GET'])
def get_student_results(exam_id: int):
    return jsonify({
        'examName': 'מבחן מועד א – אלגברה',
        'subject': 'מתמטיקה',
        'score': 8,
        'questions': [
            {
                'questionId': 1,
                'text': 'פתרו את המשוואה: 3x + 7 = 22',
                'studentAnswer': '5',
                'correctAnswer': '5',
                'isCorrect': True,
                'score': 5,
                'maxScore': 5,
            }
        ],
    })
