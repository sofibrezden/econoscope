from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

from .history import get_db_connection
from ..models import save_user, check_user_credentials
from flask_cors import CORS


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

# @bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if check_user_credentials(username, password):
#             session['username'] = username
#             return redirect(url_for('main.index'))
#         return jsonify({'error': 'Invalid username or password!'}), 400
#     return render_template('login.html')

# @bp.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         data = request.get_json()  # Parse JSON data
#         print(data)
#         username = data.get('username')
#         password = data.get('password')
#
#         if check_user_credentials(username, password):
#             session['username'] = username
#             return jsonify({"message": "Login successful"}), 200
#
#         return jsonify({'error': 'Invalid username or password!'}), 400

from flask import request, jsonify, session
from werkzeug.security import check_password_hash
import sqlite3

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check credentials in the database
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

    # Validate credentials
    if user and check_password_hash(user["password"], password):
        session['user_id'] = user["id"]  # Store user ID in session
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid username or password"}), 400



@bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user_id from the session
    return jsonify({"message": "Logout successful"}), 200

@bp.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({"authenticated": True}), 200
    else:
        return jsonify({"authenticated": False}), 401
