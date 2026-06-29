import datetime
from flask import request

import jwt
from server.config import Config


def create_token(student: dict):
    payload = {
        "student_id": student["id"],
        "role": student["role"],
        "student_name": student["student_name"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


def get_student_data():
    token = request.cookies.get("token")
    if not token:
        return None
    try:
        decoded = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    return decoded

