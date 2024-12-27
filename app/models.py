from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()
logging.basicConfig(level=logging.DEBUG)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.get(user_id)

    @staticmethod
    def save_user(user):
        try:
            db.session.add(user)
            db.session.commit()
            logging.debug(f"User {user.username} added successfully.")
        except Exception as e:
            logging.error(f"Error adding user {user.username}: {e}")
            db.session.rollback()


class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    country = db.Column(db.String(80))
    age = db.Column(db.String(50))
    sex = db.Column(db.String(50))
    year = db.Column(db.Integer)
    prediction = db.Column(db.Float)
    state = db.Column(db.String(50))


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def save_prediction(user_id, country, age, sex, year, prediction, state):
    prediction = Prediction(user_id=user_id, country=country, age=age, sex=sex,
                            year=year, prediction=prediction, state=state)
    db.session.add(prediction)
    db.session.commit()


def get_user_predictions(user_id):
    predictions = Prediction.query.filter_by(user_id=user_id).all()
    print(predictions)
    return [
        {
            "id": prediction.id,
            "country": prediction.country,
            "age": prediction.age,
            "sex": prediction.sex,
            "year": prediction.year,
            "prediction": prediction.prediction,
            "state": prediction.state,
        }
        for prediction in predictions
    ]


def delete_prediction(prediction_id):
    prediction = Prediction.query.get(prediction_id)
    if prediction:
        db.session.delete(prediction)
        db.session.commit()
