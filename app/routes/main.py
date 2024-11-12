import sqlite3

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from ..models import get_user_id, save_prediction, get_user_predictions
import pandas as pd
from flask_cors import CORS

bp = Blueprint('main', __name__)
CORS(bp)

df = pd.read_csv('result_sarima_arima.csv',
                 names=["Model", "Country", "Age", "Sex", "Date", "Forecast", "R^2", "MSE", "RMSE", "MAPE"], header=0)


def get_best_model(subset):
    return subset.loc[subset['R^2'].idxmax()]


@bp.route('/')
def index():
    countries = df['Country'].unique()
    return render_template('index.html', countries=countries)


@bp.route('/predict', methods=['POST'])
def predict():
    if request.is_json:
        data = request.get_json()
        print("Received data:", data)
        selected_country = data.get('country')
        selected_age = data.get('age')
        selected_sex = data.get('sex')
        selected_year = data.get('year')

        if not selected_country or not selected_age or not selected_sex or not selected_year:
            return jsonify({"error": "Missing required fields"}), 400

        filtered_df = df[(df['Country'] == selected_country) &
                         (df['Age'] == selected_age) &
                         (df['Sex'] == selected_sex) &
                         (df['Date'].str.startswith(str(selected_year)))]

        if filtered_df.empty:
            return jsonify({"error": "No data available for the selected criteria"}), 404

        best_model_entry = get_best_model(filtered_df)
        avg_forecast = filtered_df['Forecast'].mean()

        if 'username' in session:
            user_id = get_user_id(session['username'])
            save_prediction(user_id, selected_country, selected_age, selected_sex, selected_year,
                            best_model_entry['Model'], best_model_entry['R^2'], best_model_entry['RMSE'], avg_forecast)

        return jsonify({
            "model": best_model_entry['Model'],
            "r_squared": best_model_entry['R^2'],
            "rmse": best_model_entry['RMSE'],
            "prediction": avg_forecast
        })
    else:
        print("Invalid input format")
        return jsonify({"error": "Invalid input format, JSON expected"}), 400


@bp.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    user_id = get_user_id(session['username'])
    history_data = get_user_predictions(user_id)
    return render_template('history.html', history=history_data)


@bp.route('/api/form-data', methods=['GET'])
def get_form_data():
    countries = df['Country'].unique().tolist()
    ages = df['Age'].unique().tolist()
    sexes = df['Sex'].unique().tolist()

    return jsonify({
        "countries": countries,
        "ages": ages,
        "sexes": sexes
    })


@bp.route('/api/user-history', methods=['GET'])
def get_user_history():
    if 'username' not in session:
        return jsonify({"error": "User not authenticated"}), 401

    user_id = get_user_id(session['username'])
    history_data = get_user_predictions(user_id)

    history_list = []
    for prediction in history_data:
        history_list.append({
            "country": prediction[0],
            "age": prediction[1],
            "sex": prediction[2],
            "year": prediction[3],
            "model": prediction[4],
            "r_squared": prediction[5],
            "rmse": prediction[6],
            "forecast": prediction[7]
        })

    return jsonify(history_list)
