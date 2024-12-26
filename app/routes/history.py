from flask import Blueprint, jsonify, request
from flask_cors import CORS
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from app.models import get_user_predictions

bp = Blueprint('history', __name__)
CORS(bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

SECRET_KEY = "your_secret_key"


def get_user_id_from_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None
    try:
        payload = decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except (ExpiredSignatureError, InvalidTokenError):
        return None


@bp.route('/api/user-history', methods=['GET'])
def get_user_history():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    predictions = get_user_predictions(user_id)
    history = [
        {
            "id": prediction["id"],
            "country": prediction["country"],
            "age": prediction["age"],
            "sex": prediction["sex"],
            "year": prediction["year"],
            "prediction": prediction["prediction"],
            "state": prediction["state"],
        }
        for prediction in predictions
    ]
    return jsonify(history), 200
