
from flask import Blueprint, jsonify, session
import sqlite3
from contextlib import contextmanager

bp = Blueprint('history', __name__)

# Контекстний менеджер для роботи з базою даних
@contextmanager
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Дозволяє доступ до колонок за назвами
    conn.execute("PRAGMA foreign_keys = ON")  # Включення підтримки зовнішніх ключів
    try:
        yield conn
    finally:
        conn.close()

# Ендпоінт для отримання історії користувача, якщо він автентифікований
@bp.route('/api/user-history', methods=['GET'])
def get_user_history():
    # Перевірка, чи автентифікований користувач
    if 'user_id' not in session:
        return jsonify({"error": "User not authenticated"}), 401

    user_id = session['user_id']  # Отримання ID користувача із сесії

    # Отримання історії прогнозів з бази даних
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT country, age, sex, year, model, r_squared, rmse, prediction 
            FROM predictions 
            WHERE user_id = ?
        ''', (user_id,))
        history = cursor.fetchall()  # Отримання всіх результатів як список рядків

    # Форматування результатів у список словників
    history_list = [
        {
            "country": row["country"],
            "age": row["age"],
            "sex": row["sex"],
            "year": row["year"],
            "model": row["model"],
            "r_squared": row["r_squared"],
            "rmse": row["rmse"],
            "prediction": row["prediction"]
        }
        for row in history
    ]

    return jsonify(history_list)
