from flask import Flask
from db.db_connection import init_db
from services.grading_service import GradingService
from controllers.grading_controller import create_grading_blueprint
import os
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

init_db(app)

# 1. טוען מודל
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'my_model')
model = SentenceTransformer(MODEL_PATH)

# 2. יוצר service עם המודל
grading_service = GradingService(model=model)

# 3. רושם blueprint עם הזרקת service
app.register_blueprint(
    create_grading_blueprint(grading_service),
    url_prefix='/api/grading'
)

if __name__ == '__main__':
    app.run(debug=True, port=5000)