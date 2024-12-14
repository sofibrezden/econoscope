from flask import Flask
from flask_cors import CORS
from .models import init_db
from .routes import auth, main, history, prediction


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    CORS(app, supports_credentials=True,resources={r"/*": {"origins": "*"}},allow_headers=["Content-Type", "Authorization"])

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(history.bp)
    app.register_blueprint(prediction.bp)

    return app
