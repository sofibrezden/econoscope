from .models import init_db, db
from flask import Flask
from flask_cors import CORS
from .routes import auth, main, history, prediction

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    CORS(app, supports_credentials=True,resources={r"/*": {"origins": "*"}},allow_headers=["Content-Type", "Authorization"])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://econodata_user:Sy2OmNKLBSg03p9XuM183auV9aVRqoZr@dpg-cubq975ds78s73aefcmg-a.oregon-postgres.render.com/econodata'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(history.bp)
    app.register_blueprint(prediction.bp)

    return app
