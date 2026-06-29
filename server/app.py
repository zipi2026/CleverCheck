from flask import Flask
from controllers.subject_controller import subject_blueprint
from controllers.classes_controller import classes_blueprint
from controllers.teachers_controller import teachers_blueprint
from controllers.students_controller import students_blueprint
from controllers.exams_controller import exams_blueprint
from controllers.options_controller import options_blueprint
from controllers.question_types_controller import question_types_blueprint
from controllers.questions_controller import questions_blueprint
from controllers.student_answers_controller import student_answers_blueprint
from controllers.student_exams_controller import student_exams_blueprint
from controllers.teacher_answers_controller import teacher_answers_blueprint
from controllers.student_client_controller import student_client_bp
from flask_cors import CORS
from config import Config
from server.controllers.students_auth_controller import auth_bp
#from server.controllers.exam_classes_controller import exam_classes_blueprint
#from server.controllers.teacher_classes_controller import teacher_classes_blueprint
#from db_connection import init_db
from services.grading_service import GradingService
#from controllers.grading_controller import create_grading_blueprint
import os
from sentence_transformers import SentenceTransformer
from db_connection_test import health_check
#import server.models
from flask_cors import CORS

if health_check():
    print("DB connected successfully ✅")
else:
    print("DB connection failed ❌")

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5174"])
app.config["SECRET_KEY"] = Config.SECRET_KEY
#init_db(app)

# 1. טוען מודל
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'my_model')
model = SentenceTransformer(MODEL_PATH)

# 2. יוצר service עם המודל
grading_service = GradingService(model=model)

# 3. רושם blueprint עם הזרקת service
#app.register_blueprint(
  #  create_grading_blueprint(grading_service),
 #   url_prefix='/api/grading'
#)
app.register_blueprint(subject_blueprint, url_prefix='/api/subjects')
app.register_blueprint(classes_blueprint, url_prefix='/api/classes')
app.register_blueprint(teachers_blueprint, url_prefix='/api/teachers')
app.register_blueprint(students_blueprint, url_prefix='/api/students')
app.register_blueprint(exams_blueprint, url_prefix='/api/exams')
app.register_blueprint(options_blueprint, url_prefix='/api/options')
app.register_blueprint(questions_blueprint, url_prefix='/api/questions')
app.register_blueprint(student_answers_blueprint, url_prefix='/api/student_answers')
app.register_blueprint(student_exams_blueprint, url_prefix='/api/student_exams')
app.register_blueprint(teacher_answers_blueprint, url_prefix='/api/teacher_answers')
app.register_blueprint(question_types_blueprint, url_prefix='/api/question_types')
app.register_blueprint(auth_bp, url_prefix="/api/auth")



#app.register_blueprint(exam_classes_blueprint, url_prefix='/api/exam-classes')
#app.register_blueprint(teacher_classes_blueprint, url_prefix='/api/teacher-classes')
if __name__ == '__main__':
    app.run(host="localhost", port=5000)

#########################
# server/app.py


# רישום ה-Blueprint עם URL prefix

# רישום מנגנוני טיפול בשגיאות (אם קיימים)
