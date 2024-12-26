from flask import Blueprint, jsonify
import pandas as pd
from flask_cors import CORS
import os

bp = Blueprint('main', __name__)
CORS(bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

file_path = os.path.join(os.path.dirname(__file__), 'yearly_unemployment_data.csv')
df = pd.read_csv(file_path,
                 names=["Year", "Country", "Age", "Sex", "Forecast"], header=0)


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
