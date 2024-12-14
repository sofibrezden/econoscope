from flask import Blueprint, jsonify, request
import sqlite3
from contextlib import contextmanager
from jwt import decode, ExpiredSignatureError, InvalidTokenError

bp = Blueprint('history', __name__)
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

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT country, age, sex, year, prediction 
            FROM predictions 
            WHERE user_id = ?
        ''', (user_id,))
        history = cursor.fetchall()

    history_list = [
        {
            "country": row["country"],
            "age": row["age"],
            "sex": row["sex"],
            "year": row["year"],
            "prediction": row["prediction"]
        }
        for row in history
    ]

    return jsonify(history_list)
