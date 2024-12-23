import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        country TEXT,
                        age TEXT,
                        sex TEXT,
                        year INTEGER,
                        prediction REAL,
                        state TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                      )''')
    conn.commit()
    conn.close()

def get_user_id(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

def save_user(username, email, password):
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()
    conn.close()

def check_user_credentials(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return check_password_hash(result[0], password)
    return False

def save_prediction(user_id, country, age, sex, year, prediction, state):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM predictions WHERE user_id = ? AND country = ? AND year = ?''',
                   (user_id, country, year))
    existing_prediction = cursor.fetchone()
    if existing_prediction:
        print("Prediction already exists.")
        conn.close()
        return
    cursor.execute('''INSERT INTO predictions (user_id, country, age, sex, year, prediction, state)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (user_id, country, age, sex, year, prediction, state))
    conn.commit()
    conn.close()


def get_user_predictions(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, country, age, sex, year, prediction,state
                      FROM predictions WHERE user_id = ?''', (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history


def delete_prediction(prediction_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
    conn.commit()
    conn.close()
