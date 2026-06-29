import pytest
from flask import Flask
from server.controllers.student_client_controller import student_client_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(student_client_bp, url_prefix='/api/student')
    app.testing = True
    with app.test_client() as client:
        yield client


def test_list_student_exams(client):
    response = client.get('/api/student/exams')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['examId'] > 0


def test_get_student_exam_payload(client):
    response = client.get('/api/student/exams/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['exam']['examId'] == 1
    assert len(data['questions']) > 0


def test_save_and_submit_student_answers(client):
    response = client.post('/api/student/exams/1/answers', json={
        'studentExamId': 101,
        'questionId': 1,
        'answerText': 'תשובה לדוגמה'
    })
    assert response.status_code == 200
    submit = client.post('/api/student/exams/1/submit', json={'studentExamId': 101})
    assert submit.status_code == 200
