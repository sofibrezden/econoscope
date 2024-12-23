import sqlite3

from flask import Blueprint, jsonify, request
from .history import get_db_connection
from ..models import init_db
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "your_secret_key"

bp = Blueprint('auth', __name__)
CORS(bp,resources={r"/*": {"origins": "*"}}, supports_credentials=True)

init_db()
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    hashed_password = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed_password))
            conn.commit()
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            return jsonify({"error": "Username or email already exists"}), 400
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User registered successfully"}), 201


@bp.route('/login', methods=['POST'])
def login():
    print("Login route accessed")
    data = request.get_json()
    print(f"Received data: {data}")

    username = data.get('username')
    password = data.get('password')
    print(f"Username: {username}, Password: {password}")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

    if user and check_password_hash(user["password"], password):
        token = generate_token(user["id"])
        print("Login successful, token generated")
        return jsonify({"message": "Login successful", "token": token}), 200
    print("Invalid username or password")
    return jsonify({"error": "Invalid username or password"}), 400



@bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return jsonify({"message": "Logout successful"}), 200
        except ExpiredSignatureError:
            return jsonify({"error": "Token has already expired"}), 400
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 400
    else:
        return jsonify({"error": "No valid Authorization header found"}), 400


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # Token valid for 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Decoded payload:", payload)
        return payload["user_id"]
    except ExpiredSignatureError:
        print("Token has expired")
        return None
    except InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None



@bp.route('/check-auth', methods=['GET'])
def check_auth():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        user_id = decode_token(token)
        if user_id:
            print("User authenticated:", user_id)
            return jsonify({"authenticated": True}), 200
        else:
            print("Token validation failed")
    else:
        print("No valid Authorization header found")
    return jsonify({"authenticated": False}), 401
