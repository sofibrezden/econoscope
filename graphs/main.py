import sqlite3
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import requests
import jwt
from urllib.parse import urlparse, parse_qs
import flask
from flask import Blueprint, jsonify, request
from contextlib import contextmanager
from jwt import decode, ExpiredSignatureError, InvalidTokenError

# Load unemployment data
unemployment_data = pd.read_csv('df_long_with_coordinates.csv')

# Extract locations and prepare data
location1 = unemployment_data[['Country', 'latitude', 'longitude']]
list_locations = location1.set_index('Country')[['latitude', 'longitude']].T.to_dict('dict')

region = unemployment_data['Continent'].unique()
continent = unemployment_data['Continent'].unique()
sex_categories = ['Total', 'Male', 'Female']

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Secret key for JWT decoding
SECRET_KEY = "your_secret_key"


# Function to check user registration status
def check_user_registration():
    # Get the current URL or Referer header
    if flask.has_request_context():
        # First, check the request URL
        parsed_url = urlparse(flask.request.url)
        query_params = parse_qs(parsed_url.query)

        # If token is not in URL, check the Referer header
        if 'token' not in query_params and 'Referer' in flask.request.headers:
            referer_url = flask.request.headers.get('Referer')
            parsed_url = urlparse(referer_url)
            query_params = parse_qs(parsed_url.query)

        # Check if JWT token is in parameters
        if 'token' in query_params:
            token = query_params['token'][0]
            try:
                # Decode JWT token to verify
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                # Check if user is registered (conditionally check token payload)
                if 'user_id' in decoded_token:
                    return True, decoded_token['user_id']
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                return False, None
    return False, None


# Database connection context manager
@contextmanager
def get_db_connection():
    conn = sqlite3.connect('../users.db')
    conn.row_factory = sqlite3.Row  # Allows access to columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
    try:
        print("connected")
        yield conn
    finally:
        conn.close()


# Function to get user prediction history
def get_user_history():
    is_authenticated, user_id = check_user_registration()
    if not is_authenticated:
        print("User not authenticated or token invalid.")
        return []

    # Fetch prediction history from the database
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT country, age, sex, year, model, r_squared, rmse, prediction 
                FROM predictions 
                WHERE user_id = ?
            ''', (user_id,))
            history = cursor.fetchall()  # Get all results as a list of rows
            print(f"Fetched {len(history)} predictions for user ID {user_id}.")
        except sqlite3.Error as e:
            print(f"Error fetching predictions: {e}")
            return []

    # Convert history rows to a list of dictionaries
    history_list = [
        {
            "country": row["country"],
            "age": row["age"],
            "sex": row["sex"],
            "year": row["year"],
            "model": row["model"],
            "r_squared": row["r_squared"],
            "rmse": row["rmse"],
            "prediction": row["prediction"]
        }
        for row in history
    ]

    return history_list


# Example route to get user history
@server.route('/user/history', methods=['GET'])
def user_history():
    history = get_user_history()
    if not history:
        return jsonify({"error": "User not authenticated"}), 401
    return jsonify(history)


def serve_layout():
    is_authenticated, user_id = check_user_registration()
    layout_children = []

    # Додаткові графіки для аналізу
    layout_children.append(
        html.Div([
            html.Div([
                html.P('Select Year:', className='fix_label', style={'color': '#627254', 'margin-left': '1%'}),
                dcc.Slider(id='select_year',
                           min=2014,
                           max=2024,
                           value=2024,
                           marks={year: {'label': str(year), 'style': {'color': '#627254', 'font-size': '20px'}} for
                                  year in
                                  range(2014, 2025, 1)},
                           step=1),
            ], className="create_container 12 columns"),
        ], className="row flex-display", style={"margin-bottom": "25px"})
    )

    # Карта для вибору континенту
    layout_children.append(
        html.Div([
            html.Div([
                html.P('Select Continent:', className='fix_label', style={'color': '#627254', 'font-weight': 'bold'}),
                dcc.Dropdown(id='w_continent',
                             multi=False,
                             clearable=True,
                             disabled=False,
                             style={'display': True},
                             value='Europe',
                             placeholder='Select Continent',
                             options=[{'label': c, 'value': c}
                                      for c in continent], className='dcc_compon'),
                html.P('Select Gender:', className='fix_label', style={'color': '#627254', 'font-weight': 'bold'}),
                dcc.Dropdown(id='w_gender',
                             multi=False,
                             clearable=True,
                             disabled=False,
                             style={'display': True},
                             value='Total',
                             placeholder='Select Gender',
                             options=[{'label': gender, 'value': gender}
                                      for gender in sex_categories], className='dcc_compon'),
            ], className="create_container three columns", style={"margin-bottom": "25px"}),
            html.Div([
                dcc.Graph(id='map_continent',
                          config={'displayModeBar': 'hover'}),
            ], className="create_container twelve columns"),
        ], className="row flex-display", style={"margin-top": "25px"})
    )

    # Графіки бар-лінія та кругова діаграма
    layout_children.append(
        html.Div([
            html.Div([
                dcc.Graph(id='bar_line_chart',
                          config={'displayModeBar': 'hover'}, style={'color': '#627254'}),
            ], className="create_container six columns"),
            html.Div([
                dcc.Graph(id='pie_chart',
                          config={'displayModeBar': 'hover'}),
            ], className="create_container six columns"),
        ], className="row flex-display")
    )

    # Add hidden components for `w_year` and `w_prediction` to avoid callback issues
    layout_children.append(
        html.Div([
            dcc.Dropdown(id='w_year', multi=False, clearable=False, style={'display': 'none'}),
            dcc.Dropdown(id='w_prediction', multi=False, clearable=False, style={'display': 'none'}),
        ])
    )

    # Додайте останню секцію лише якщо користувач зареєстрований
    if is_authenticated:
        layout_children.append(
            html.Div([
                html.Div([
                    html.P('Select Year:', className='fix_label', style={'color': '#627254', 'font-weight': 'bold'}),
                    dcc.Dropdown(id='w_year',
                                 multi=False,
                                 clearable=False,
                                 disabled=False,
                                 style={'display': True},
                                 value=2025,
                                 placeholder='Select Year',
                                 options=[{'label': str(year), 'value': year}
                                          for year in range(2025, 2028)], className='dcc_compon'),
                    html.P("Select predictions from your history (Country, Age, Sex):", className='fix_label',
                           style={'color': '#627254', 'font-weight': 'bold'}),
                    dcc.Dropdown(id='w_prediction',
                                 multi=False,
                                 clearable=True,
                                 disabled=False,
                                 style={'display': True},
                                 placeholder='Select Prediction',
                                 options=[],
                                 value=None,
                                 className='dcc_compon'),
                ], className="create_container three columns", style={"margin-bottom": "25px"}),
                html.Div([
                    dcc.Graph(id='unemployment_rate_graph',
                              config={'displayModeBar': 'hover'}, style={'color': '#627254'}),
                ], className="create_container nine columns"),
            ], className="row flex-display", style={"margin-top": "25px"})
        )

    return html.Div(layout_children, id="mainContainer", style={"display": "flex", "flex-direction": "column"})


app.layout = serve_layout


@app.callback(Output('w_prediction', 'options'),
              [Input('w_year', 'value')])
def update_prediction_dropdown(w_year):
    user_predictions = get_user_history()
    # Filter countries, age, and sex that were predicted in the selected year
    predictions = [
        {
            'label': f"{prediction['country']}, {prediction['age']}, {prediction['sex']}",
            'value': f"{prediction['country']}|{prediction['age']}|{prediction['sex']}"
        }
        for prediction in user_predictions if prediction.get('year') == w_year
    ]
    if predictions:
        return predictions
    return [{'label': 'No predictions available', 'value': ""}]


@app.callback(Output('w_prediction', 'value'),
              [Input('w_prediction', 'options')])
def set_default_prediction(options):
    if options and options[0]['value'] is not None:
        return options[0]['value']
    return None


# Create map for continent selection
@app.callback(Output('map_continent', 'figure'),
              [Input('w_continent', 'value')],
              [Input('select_year', 'value')],
              [Input('w_gender', 'value')])
def update_continent_map(w_continent, select_year, w_gender):
    terr3 = unemployment_data[(unemployment_data['Continent'] == w_continent) &
                              (unemployment_data['Year'] == select_year) &
                              (unemployment_data['Sex'] == w_gender)]

    if not terr3.empty:
        zoom_lat = terr3['latitude'].mean()
        zoom_lon = terr3['longitude'].mean()
        zoom = 3
    else:
        zoom_lat = 20
        zoom_lon = 0
        zoom = 1.5

    return {
        'data': [
            go.Scattermapbox(
                lon=terr3['longitude'],
                lat=terr3['latitude'],
                mode='markers+text',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color=terr3['UnemploymentRate'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(
                        title="Unemployment Rate", titlefont=dict(color='#627254'),
                        titleside='right',
                        x=0.95,
                        xanchor='left',
                        thickness=15,
                        len=0.7
                    )
                ),
                text=terr3['Country'],
                hoverinfo='text',
                hovertext=
                '<b>Region</b>: ' + terr3['Continent'].astype(str) + '<br>' +
                '<b>Country</b>: ' + terr3['Country'].astype(str) + '<br>' +
                '<b>Unemployment Rate</b>: ' + terr3['UnemploymentRate'].astype(str) + '<br>' +
                '<b>Longitude</b>: ' + terr3['longitude'].astype(str) + '<br>' +
                '<b>Latitude</b>: ' + terr3['latitude'].astype(str) + '<br>' +
                '<b>Year</b>: ' + terr3['Year'].astype(str) + '<br>'
            )
        ],

        'layout': go.Layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            hovermode='closest',
            mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                # Use mapbox token here
                center=go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_lon),
                style='light',
                zoom=zoom
            ),
            autosize=True,
        )
    }


@app.callback(Output('bar_line_chart', 'figure'),
              [Input('w_continent', 'value')],
              [Input('select_year', 'value')],
              [Input('w_gender', 'value')])
def update_bar_line_chart(w_continent, select_year, w_gender):
    filtered_data = unemployment_data[(unemployment_data['Continent'] == w_continent) &
                                      (unemployment_data['Year'] <= select_year) &
                                      (unemployment_data['Sex'] == w_gender)]
    grouped_data = filtered_data.groupby('Country')['UnemploymentRate'].mean().reset_index()

    return {
        'data': [
            go.Bar(
                x=grouped_data['Country'],
                y=grouped_data['UnemploymentRate'],
                marker=dict(color='#626058'),
                name='Unemployment Rate      ',
                hoverinfo='text',
                hovertext='<b>Country</b>: ' + grouped_data['Country'] + '<br>' +
                          '<b>Unemployment Rate</b>: ' + grouped_data['UnemploymentRate'].astype(str) + '<br>'
            ),
            go.Scatter(
                x=grouped_data['Country'],
                y=grouped_data['UnemploymentRate'],
                mode='lines+markers',
                line=dict(color='#626058', width=2),
                marker=dict(size=5, color='#626058'),
                name='Trend Line',
                hoverinfo='text',
                hovertext='<b>Country</b>: ' + grouped_data['Country'] + '<br>' +
                          '<b>Unemployment Rate</b>: ' + grouped_data['UnemploymentRate'].astype(str) + '<br>'
            )
        ],
        'layout': go.Layout(
            title='Unemployment Rate by Country up to ' + str(select_year),
            titlefont=dict(color='#626058', size=20),
            xaxis=dict(title='<b>Country</b>', color='#627254', showline=True, linewidth=2, tickangle=-45,
                       tickfont=dict(
                           size=10
                       )),
            yaxis=dict(title='<b>Unemployment Rate</b>', color='#627254', showline=True, linewidth=2),
            plot_bgcolor='#f9f9f9',
            paper_bgcolor='#f9f9f9',
            hovermode='closest',
            autosize=True,
            legend=dict(
                orientation='h',
                x=0.5,
                xanchor='center',
                y=1.1,
                traceorder='normal',
                font=dict(
                    size=12
                )
            )
        )
    }


# Create pie chart for continent unemployment rate distribution
@app.callback(Output('pie_chart', 'figure'),
              [Input('select_year', 'value')])
def update_pie_chart(select_year):
    filtered_data = unemployment_data[unemployment_data['Year'] <= select_year]
    continent_unemployment = filtered_data.groupby('Continent')['UnemploymentRate'].mean().reset_index()

    return {
        'data': [
            go.Pie(
                labels=continent_unemployment['Continent'],
                values=continent_unemployment['UnemploymentRate'],
                marker=dict(colors=['#FF00FF', '#9C0C38', 'orange', 'green', 'blue', 'purple']),
                hoverinfo='label+value+percent',
                textinfo='label+value',
                textfont=dict(size=13)
            )
        ],
        'layout': go.Layout(
            title='Average Unemployment Rate by Continent up to ' + str(select_year),
            titlefont=dict(color='#627254', size=20),
            plot_bgcolor='#f9f9f9',
            paper_bgcolor='#f9f9f9',
            legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.1),
            hovermode='closest'
        )
    }


@app.callback(Output('unemployment_rate_graph', 'figure'),
              [Input('w_prediction', 'value')])
def update_unemployment_rate_graph(w_prediction):
    if not w_prediction:
        return go.Figure()

    country, age, sex = w_prediction.split('|')
    filtered_data = unemployment_data[(unemployment_data['Country'] == country) &
                                      (unemployment_data['Age'] == age) &
                                      (unemployment_data['Sex'] == sex)]

    return {
        'data': [
            go.Scatter(
                x=filtered_data['Year'],
                y=filtered_data['UnemploymentRate'],
                mode='lines+markers',
                line=dict(color='#627254', width=2),
                marker=dict(size=5, color='#627254'),
                name='Unemployment Rate',
                hoverinfo='text',
                hovertext='<b>Year</b>: ' + filtered_data['Year'].astype(str) + '<br>' +
                          '<b>Unemployment Rate</b>: ' + filtered_data['UnemploymentRate'].astype(str) + '<br>'
            )
        ],
        'layout': go.Layout(
            title=f'Unemployment Rate Over Time for {country}, {age}, {sex}',
            titlefont=dict(color='#627254', size=20),
            xaxis=dict(title='<b>Year</b>', color='#DDDDDD', showline=True, linewidth=2),
            yaxis=dict(title='<b>Unemployment Rate</b>', color='#DDDDDD', showline=True, linewidth=2),
            plot_bgcolor='#f9f9f9',
            paper_bgcolor='#f9f9f9',
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
