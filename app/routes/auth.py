from flask import Blueprint, render_template, redirect, url_for, jsonify, session, request
from .history import get_db_connection
from ..models import save_user
from flask_cors import CORS
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "your_secret_key"

bp = Blueprint('auth', __name__)
CORS(bp, supports_credentials=True, origins=["http://localhost:3000"])


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            save_user(username, password)
            return redirect(url_for('auth.login'))
        except:
            return jsonify({'error': 'Username already exists!'}), 400
    return render_template('register.html')


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

    if user and check_password_hash(user["password"], password):
        token = generate_token(user["id"])
        return jsonify({"message": "Login successful", "token": token}), 200

    return jsonify({"error": "Invalid username or password"}), 400



@bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]  # Забираємо тільки сам токен без "Bearer"
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
        print("Decoded payload:", payload)  # Додаткове логування для перевірки токену
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
        token = token.split(" ")[1]  # Забираємо тільки сам токен без "Bearer"
        user_id = decode_token(token)
        if user_id:
            print("User authenticated:", user_id)
            return jsonify({"authenticated": True}), 200
        else:
            print("Token validation failed")
    else:
        print("No valid Authorization header found")
        # Тимчасовий код для тестування
        # return jsonify({"authenticated": True}), 200

    return jsonify({"authenticated": False}), 401
