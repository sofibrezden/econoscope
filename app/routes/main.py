from flask import Blueprint, render_template, jsonify
import pandas as pd
from flask_cors import CORS

bp = Blueprint('main', __name__)
CORS(bp, supports_credentials=True, origins="http://localhost:3000")  # Enable credentials support),

df = pd.read_csv('result_sarima_arima.csv',
                 names=["Model", "Country", "Age", "Sex", "Date", "Forecast", "R^2", "MSE", "RMSE", "MAPE"], header=0)


def get_best_model(subset):
    return subset.loc[subset['R^2'].idxmax()]


@bp.route('/')
def index():
    countries = df['Country'].unique()
    return render_template('index.html', countries=countries)


@bp.route('/form-data', methods=['GET'])
def get_form_data():
    countries = df['Country'].unique().tolist()
    ages = df['Age'].unique().tolist()
    sexes = df['Sex'].unique().tolist()

    return jsonify({
        "countries": countries,
        "ages": ages,
        "sexes": sexes
    })
