import pandas as pd
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from ..models import save_prediction, delete_prediction

bp = Blueprint('prediction', __name__)
CORS(bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

SECRET_KEY = "your_secret_key"

df = pd.read_csv('yearly_unemployment_data.csv',
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
        forecast_2023 = df[(df['Country'] == selected_country) &
                           (df['Age'] == selected_age) &
                           (df['Sex'] == selected_sex) &
                           (df['Year'] == 2023)]['Forecast']
        print(forecast_2023)
        if not forecast_2023.empty:
            forecast_2023 = forecast_2023.iloc[0]
            if avg_forecast > forecast_2023:
                state = "Growth"
            elif avg_forecast < forecast_2023:
                state = "Decline"
            else:
                state = "Stability"
        print(state)
        return jsonify({
            "prediction": avg_forecast,
            "country": selected_country,
            "age": selected_age,
            "sex": selected_sex,
            "year": selected_year,
            "state": state,
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
        state = data.get('state')

        if not all([prediction, selected_country, selected_age, selected_sex, selected_year]):
            return jsonify({"error": "Missing required fields"}), 400

        save_prediction(user_id, selected_country, selected_age, selected_sex, selected_year,
                        prediction, state)

        return jsonify({"message": "Prediction saved successfully", "state": state}), 200
    else:
        return jsonify({"error": "Invalid input format, JSON expected"}), 400


@bp.route('/delete-prediction', methods=['DELETE'])
def delete_prediction_endpoint():
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "User not authenticated"}), 401

        data = request.get_json()
        prediction_id = data.get('prediction_id')

        if not prediction_id:
            return jsonify({"error": "Missing prediction_id"}), 400

        delete_prediction(prediction_id)
        return jsonify({"message": "Prediction deleted successfully"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Internal server error"}), 500
