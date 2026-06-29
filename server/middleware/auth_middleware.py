import jwt
from functools import wraps
from flask import request, jsonify
from config import Config
import datetime


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        token = request.cookies.get("token")

        if not token:
            return jsonify({"error": "אין טוקן"}), 401

        try:
            data = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = data  # שומרים את המשתמש לבפנים

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "טוקן פג תוקף"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "טוקן לא תקין"}), 401

        return f(*args, **kwargs)

    return wrapper


