import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # server/
MODEL_PATH = os.path.join(BASE_DIR, "my_model")

print(os.listdir(MODEL_PATH))