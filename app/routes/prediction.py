import pandas as pd
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from ..models import save_prediction

bp = Blueprint('prediction', __name__)
CORS(bp, supports_credentials=True, origins="http://localhost:3000")

SECRET_KEY = "your_secret_key"


df = pd.read_csv('../yearly_unemployment_data.csv',
                 names=["Year", "Country", "Age", "Sex", "Forecast"], header=0)


def get_user_id_from_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None

    try:
        decoded = decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        return decoded.get("user_id")
    except (ExpiredSignatureError, InvalidTokenError):
        return None


@bp.route('/prepare-predict', methods=['POST'])
def prepare_predict():
    if request.is_json:
        data = request.get_json()
        print("Received data:", data)
        selected_country = data.get('country')
        selected_age = data.get('age')
        selected_sex = data.get('sex')
        selected_year = data.get('year')
        if not all([selected_country, selected_age, selected_sex, selected_year]):
            return jsonify({"error": "Missing required fields"}), 400

        filtered_df = df[(df['Country'] == selected_country) &
                         (df['Age'] == selected_age) &
                         (df['Sex'] == selected_sex) &
                         (df['Year'] == int(selected_year))]

        if filtered_df.empty:
            return jsonify({"error": "No data available for the selected criteria"}), 404

        avg_forecast = filtered_df['Forecast'].mean()

        return jsonify({
            "prediction": avg_forecast,
            "country": selected_country,
            "age": selected_age,
            "sex": selected_sex,
            "year": selected_year
        })
    else:
        print("Invalid input format")
        return jsonify({"error": "Invalid input format, JSON expected"}), 400


@bp.route('/save-prediction', methods=['POST'])
def save_prediction_endpoint():
    user_id = get_user_id_from_token()
    if not user_id:
        print("No authenticated user, skipping save")
        return jsonify({"message": "Prediction not saved, user not authenticated"}), 200

    if request.is_json:
        data = request.get_json()
        prediction = data.get('prediction')
        selected_country = data.get('country')
        selected_age = data.get('age')
        selected_sex = data.get('sex')
        selected_year = data.get('year')

        if not all([prediction, selected_country, selected_age, selected_sex, selected_year]):
            return jsonify({"error": "Missing required fields"}), 400

        save_prediction(user_id, selected_country, selected_age, selected_sex, selected_year,
                        prediction)
        return jsonify({"message": "Prediction saved successfully"}), 200
    else:
        return jsonify({"error": "Invalid input format, JSON expected"}), 400
