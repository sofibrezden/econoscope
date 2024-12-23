from flask import Blueprint, jsonify
import pandas as pd
from flask_cors import CORS

bp = Blueprint('main', __name__)
CORS(bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

df = pd.read_csv('yearly_unemployment_data.csv',
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
