from flask import Blueprint, jsonify, request
import sqlite3
from contextlib import contextmanager
from flask_cors import CORS
from jwt import decode, ExpiredSignatureError, InvalidTokenError

from app.models import get_user_predictions

bp = Blueprint('history', __name__)
CORS(bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

SECRET_KEY = "your_secret_key"


@contextmanager
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def get_user_id_from_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None

    try:
        payload = decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except (ExpiredSignatureError, InvalidTokenError):
        return None


@bp.route('/api/user-history', methods=['GET'])
def get_user_history():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    predictions = get_user_predictions(user_id)
    print(predictions)
    history = [
        {
            "id": row[0],
            "country": row[1],
            "age": row[2],
            "sex": row[3],
            "year": row[4],
            "prediction": row[5],
            "state": row[6],
        }
        for row in predictions
    ]

    return jsonify(history), 200
