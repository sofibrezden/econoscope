from ..models import User
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "your_secret_key"

bp = Blueprint('auth', __name__)
CORS(bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except ExpiredSignatureError:
        print("Token has expired")
        return None
    except InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user_by_email = User.get_user_by_email(email)
    if existing_user_by_email:
        return jsonify({"error": "User with this email already exists"}), 409

    existing_user_by_name = User.get_user_by_username(username)
    if existing_user_by_name:
        return jsonify({"error": "Username already taken"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    User.save_user(new_user)

    return jsonify({"message": "User registered successfully"}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.get_user_by_username(username)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(user.id)
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200


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


@bp.route('/check-auth', methods=['GET'])
def check_auth():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"authenticated": False, "user_id": None}), 401
    token = token.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return jsonify({"authenticated": False, "user_id": None}), 401
    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({"authenticated": False, "user_id": None}), 401
    return jsonify({"authenticated": True, "user_id": user_id}), 200
