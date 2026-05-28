#from server.models import *
from flask import Flask
#from db_connection import init_db
#from services.grading_service import GradingService
#from controllers.grading_controller import create_grading_blueprint
import os
from sentence_transformers import SentenceTransformer
from db_connection_test import health_check
from controllers.subject_controller import subject_blueprint
from controllers.classes_controller import classes_blueprint
import server.models
if health_check():
    print("DB connected successfully ✅")
else:
    print("DB connection failed ❌")

app = Flask(__name__)
#import server.models
#import server.models.classes
#import server.models.student
#import server.models.exam_class
#import server.models.teacher_class
#init_db(app)

# 1. טוען מודל
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#MODEL_PATH = os.path.join(BASE_DIR, 'my_model')
#model = SentenceTransformer(MODEL_PATH)

# 2. יוצר service עם המודל
#grading_service = GradingService(model=model)

# 3. רושם blueprint עם הזרקת service
#app.register_blueprint(
  #  create_grading_blueprint(grading_service),
 #   url_prefix='/api/grading'
#)

app.register_blueprint(subject_blueprint, url_prefix='/api/subjects')
app.register_blueprint(classes_blueprint, url_prefix='/api/classes')
#app.register_blueprint(classes_blueprint, url_prefix='/classes')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

#########################
# server/app.py


# רישום ה-Blueprint עם URL prefix

# רישום מנגנוני טיפול בשגיאות (אם קיימים)
