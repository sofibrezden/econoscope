from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

from ..models import save_user, check_user_credentials
from flask_cors import CORS


bp = Blueprint('auth', __name__)
CORS(bp)

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

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user_credentials(username, password):
            session['username'] = username
            return redirect(url_for('main.index'))
        return jsonify({'error': 'Invalid username or password!'}), 400
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.index'))
