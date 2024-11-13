from flask import Flask
from flask_cors import CORS

from .models import init_db
from .routes import auth, main, history, prediction


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    # CORS configuration
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    # Session configuration for cross-origin requests
    app.config.update(
        SESSION_COOKIE_SAMESITE="None",  # Required for cross-origin cookies
        SESSION_COOKIE_SECURE=True,  # Set to True for HTTPS in production
        SESSION_COOKIE_HTTPONLY=True  # Prevents JavaScript access to cookies
    )
    # Ініціалізація бази даних
    init_db()

    # Реєстрація блакитей для маршрутів
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(history.bp)
    app.register_blueprint(prediction.bp)

    return app
