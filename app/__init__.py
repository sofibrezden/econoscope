from flask import Flask
from .models import init_db
from .routes import auth, main


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # Ініціалізація бази даних
    init_db()

    # Реєстрація блакитей для маршрутів
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    return app
