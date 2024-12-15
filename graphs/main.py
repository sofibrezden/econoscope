import sqlite3
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import jwt
from urllib.parse import urlparse, parse_qs
import flask
from flask import jsonify
from contextlib import contextmanager

unemployment_data = pd.read_csv('data/df_long_with_coordinates.csv')
df = pd.read_csv('../yearly_unemployment_data.csv')
location1 = unemployment_data[['Country', 'latitude', 'longitude']]
list_locations = location1.set_index('Country')[['latitude', 'longitude']].T.to_dict('dict')

region = unemployment_data['Continent'].unique()
continent = unemployment_data['Continent'].unique()
sex_categories = ['Total', 'Male', 'Female']

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

SECRET_KEY = "your_secret_key"


def check_user_registration():
    if flask.has_request_context():
        parsed_url = urlparse(flask.request.url)
        query_params = parse_qs(parsed_url.query)
        if 'token' not in query_params and 'Referer' in flask.request.headers:
            referer_url = flask.request.headers.get('Referer')
            parsed_url = urlparse(referer_url)
            query_params = parse_qs(parsed_url.query)

        if 'token' in query_params:
            token = query_params['token'][0]
            try:
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if 'user_id' in decoded_token:
                    return True, decoded_token['user_id']
                else:
                    print("Token decoded but 'user_id' not found in payload.")
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
                print(f"JWT decoding failed: {e}")
                return False, None
    return False, None


@contextmanager
def get_db_connection():
    conn = sqlite3.connect('../users.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        print("Database connected")
        yield conn
    finally:
        conn.close()


def get_user_history(user_id):
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT country, age, sex, year, prediction 
                FROM predictions 
                WHERE user_id = ?
            ''', (user_id,))
            history = cursor.fetchall()
            print(f"Fetched {len(history)} predictions for user ID {user_id}.")
        except sqlite3.Error as e:
            print(f"Error fetching predictions: {e}")
            return []

    history_list = [
        {
            "country": row["country"],
            "age": row["age"],
            "sex": row["sex"],
            "year": row["year"],
            "prediction": row["prediction"]
        }
        for row in history
    ]

    year_distribution = pd.DataFrame(history_list)['year'].value_counts().to_dict()
    print(f"Year distribution: {year_distribution}")

    return history_list


@server.route('/user/history', methods=['GET'])
def user_history_route():
    is_authenticated, user_id = check_user_registration()
    if not is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401
    history = get_user_history(user_id)
    return jsonify(history)


def serve_layout():
    is_authenticated, user_id = check_user_registration()
    print(f"Is authenticated: {is_authenticated}, User ID: {user_id}")
    layout_children = [html.Div([
        html.Div([
            html.P('Select Year:', className='fix_label', style={'color': '#627254', 'margin-left': '1%'}),
            dcc.Slider(
                id='select_year',
                min=2014,
                max=2024,
                value=2024,
                marks={year: {'label': str(year), 'style': {'color': '#627254', 'font-size': '20px'}} for year in
                       range(2014, 2025)},
                step=1,
            ),
        ], className="create_container 12 columns"),
    ], className="row flex-display", style={"margin-bottom": "25px"}), html.Div([
        html.Div([
            html.P('Select Continent:', className='first_section', style={'color': '#627254', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='w_continent',
                multi=False,
                clearable=True,
                disabled=False,
                value='Europe',
                placeholder='Select Continent',
                options=[{'label': c, 'value': c} for c in continent],
                className='dcc_compon'
            ),
            html.P('Select Gender:', className='first_section', style={'color': '#627254', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='w_gender',
                multi=False,
                clearable=True,
                disabled=False,
                value='Total',
                placeholder='Select Gender',
                options=[{'label': gender, 'value': gender} for gender in sex_categories],
                className='dcc_compon'
            ),
        ], className="create_container three columns", style={"margin-bottom": "25px"}),
        html.Div([
            dcc.Graph(
                id='map_continent',
                config={'displayModeBar': 'hover'},
            ),
        ], className="create_container twelve columns"),
    ], className="row flex-display", style={"margin-top": "25px"}), html.Div([
        html.Div([
            dcc.Graph(
                id='bar_line_chart',
                config={'displayModeBar': 'hover'},
                style={'color': '#627254'}
            ),
        ], className="create_container six columns"),
        html.Div([
            dcc.Graph(
                id='pie_chart',
                config={'displayModeBar': 'hover'},
            ),
        ], className="create_container six columns"),
    ], className="row flex-display"), html.Div([
        dcc.Store(id='w_year', data=None),
    ], style={'display': 'none'})]

    if is_authenticated:
        layout_children.append(
            html.Div([
                html.Div([
                    html.P(
                        "Select predictions from history (Country, Age, Sex):",
                        className='third_section',
                        style={'color': '#627254', 'font-weight': 'bold'}
                    ),
                    dcc.Dropdown(
                        id='w_prediction',
                        multi=False,
                        clearable=True,
                        disabled=False,
                        placeholder='Select Prediction',
                        options=[],
                        value=None,
                        className='dcc_compon',
                        style={
                            'font-size': '14px'
                        }

                    ),
                ], className="create_container three columns", style={"margin-bottom": "25px"}),
                html.Div([
                    dcc.Graph(
                        id='unemployment_rate_graph',
                        config={'displayModeBar': 'hover'},
                        style={'color': '#627254'}
                    ),
                ], className="create_container nine columns"),
            ], className="row flex-display", style={"margin-top": "25px"})
        )
    else:
        print("User is not authenticated. Authenticated section will not be displayed.")

    return html.Div(layout_children, id="mainContainer", style={"display": "flex", "flex-direction": "column"})


app.layout = serve_layout


@app.callback(
    Output('w_year', 'data'),
    [Input('select_year', 'value')]
)
def sync_year_store(select_year):
    print(f"Selected year: {select_year}")
    return select_year


@app.callback(
    Output('w_prediction', 'options'),
    [Input('w_year', 'data')],
    prevent_initial_call=True
)
def update_prediction_dropdown(w_year):
    print("update_prediction_dropdown called")

    is_authenticated, user_id = check_user_registration()
    if not is_authenticated:
        print("User is not authenticated within callback.")
        return [{'label': 'User not authenticated', 'value': ""}]

    user_predictions = get_user_history(user_id)
    print(f"Total user predictions: {len(user_predictions)}")

    predictions = [
        {
            'label': f"{prediction['country']}, {prediction['age']}, {prediction['sex']}, {prediction['year']}",
            'value': f"{prediction['country']}|{prediction['age']}|{prediction['sex']}|{prediction['year']}"
        }
        for prediction in user_predictions
    ]

    if predictions:
        print(f"Available predictions: {predictions}")
        return predictions
    return [{'label': 'No predictions available', 'value': ""}]


@app.callback(
    Output('w_prediction', 'value'),
    [Input('w_prediction', 'options')]
)
def set_default_prediction(options):
    print(f"set_default_prediction called with options={options}")
    if options and options[0]['value']:
        return options[0]['value']
    return None


@app.callback(
    Output('map_continent', 'figure'),
    [Input('w_continent', 'value'),
     Input('select_year', 'value'),
     Input('w_gender', 'value')]
)
def update_continent_map(w_continent, select_year, w_gender):
    terr3 = unemployment_data[
        (unemployment_data['Continent'] == w_continent) &
        (unemployment_data['Year'] == select_year) &
        (unemployment_data['Sex'] == w_gender)
        ]

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
                        title="Unemployment Rate",
                        titlefont=dict(color='#627254'),
                        titleside='right',
                        x=0.95,
                        xanchor='left',
                        thickness=15,
                        len=0.7
                    )
                ),
                text=terr3['Country'],
                hoverinfo='text',
                hovertext=(
                        '<b>Region</b>: ' + terr3['Continent'].astype(str) + '<br>' +
                        '<b>Country</b>: ' + terr3['Country'].astype(str) + '<br>' +
                        '<b>Unemployment Rate</b>: ' + terr3['UnemploymentRate'].astype(str) + '<br>' +
                        '<b>Year</b>: ' + terr3['Year'].astype(str) + '<br>'
                )
            )
        ],

        'layout': go.Layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            hovermode='closest',
            mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center=go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_lon),
                style='light',
                zoom=zoom
            ),
            autosize=True,
        )
    }


@app.callback(
    Output('bar_line_chart', 'figure'),
    [Input('w_continent', 'value'),
     Input('select_year', 'value'),
     Input('w_gender', 'value')]
)
def update_bar_line_chart(w_continent, select_year, w_gender):
    filtered_data = unemployment_data[
        (unemployment_data['Continent'] == w_continent) &
        (unemployment_data['Year'] <= select_year) &
        (unemployment_data['Sex'] == w_gender)
        ]
    grouped_data = filtered_data.groupby('Country')['UnemploymentRate'].mean().reset_index()

    grouped_data['ShortCountry'] = grouped_data['Country'].apply(
        lambda x: x if len(x) <= 15 else x[:15] + '.'
    )

    return {
        'data': [
            go.Bar(
                x=grouped_data['ShortCountry'],
                y=grouped_data['UnemploymentRate'],
                marker=dict(color='#626058'),
                name='Unemployment Rate',
                hoverinfo='text',
                hovertext=(
                        '<b>Country</b>: ' + grouped_data['Country'] + '<br>' +
                        '<b>Unemployment Rate</b>: ' + grouped_data['UnemploymentRate'].astype(str) + '<br>'
                )
            ),
            go.Scatter(
                x=grouped_data['ShortCountry'],
                y=grouped_data['UnemploymentRate'],
                mode='lines+markers',
                line=dict(color='#577564', width=2),
                marker=dict(size=5, color='#626058'),
                name='Trend Line',
                hoverinfo='text',
                hovertext=(
                        '<b>Country</b>: ' + grouped_data['Country'] + '<br>' +
                        '<b>Unemployment Rate</b>: ' + grouped_data['UnemploymentRate'].astype(str) + '<br>'
                )
            )
        ],
        'layout': go.Layout(
            title='Unemployment Rate by Country up to ' + str(select_year),
            titlefont=dict(color='#626058', size=20),
            xaxis=dict(
                title='<b>Country</b>',
                color='#627254',
                showline=True,
                linewidth=2,
                tickangle=-45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                title='<b>Unemployment Rate</b>',
                color='#627254',
                showline=True,
                linewidth=2
            ),
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
                font=dict(size=12)
            )
        )
    }


@app.callback(
    Output('pie_chart', 'figure'),
    [Input('select_year', 'value'),
     Input('w_continent', 'value')]
)
def update_pie_chart(year, continent):
    male_unemployment_rate = unemployment_data[
        (unemployment_data['Sex'] == 'Male') &
        (unemployment_data['Year'] == year) &
        (unemployment_data['Continent'] == continent)
        ]['UnemploymentRate'].sum()

    female_unemployment_rate = unemployment_data[
        (unemployment_data['Sex'] == 'Female') &
        (unemployment_data['Year'] == year) &
        (unemployment_data['Continent'] == continent)
        ]['UnemploymentRate'].sum()

    total_unemployment_rate = male_unemployment_rate + female_unemployment_rate

    if total_unemployment_rate == 0:
        return {
            'data': [],
            'layout': {
                'title': f'Unemployment Rate Distribution in {continent}, {year}',
                'annotations': [{'text': 'No data available', 'x': 0.5, 'y': 0.5, 'showarrow': False}]
            }
        }

    percent_male = (male_unemployment_rate * 100) / total_unemployment_rate
    percent_female = (female_unemployment_rate * 100) / total_unemployment_rate

    fig = {
        'data': [
            {
                'values': [percent_male, percent_female],
                'labels': ['Male', 'Female'],
                'type': 'pie',
                'marker': {'colors': ['#626058', '#6A8E7C']},
                'hoverinfo': 'label+percent+value',
                'textinfo': 'label+percent',
                'textfont': {'color': 'white', 'size': 16}
            }
        ],
        'layout': {
            'title': f'Unemployment Rate Distribution in {continent}, {year}',
            'showlegend': True
        }
    }

    return fig


@app.callback(
    Output('unemployment_rate_graph', 'figure'),
    [Input('w_prediction', 'value')]
)
def update_unemployment_rate_graph(w_prediction):
    print(f"update_unemployment_rate_graph called with w_prediction={w_prediction}")
    if not w_prediction:
        print("No prediction selected.")
        return go.Figure()

    try:
        country, age, sex, year = w_prediction.split('|')
        year = int(year)
        print(f"Parsed Prediction - Country: {country}, Age: {age}, Sex: {sex}, Year: {year}")
    except ValueError:
        print("Error parsing w_prediction.")
        return go.Figure()

    is_authenticated, user_id = check_user_registration()
    if not is_authenticated:
        print("User is not authenticated within callback.")
        return go.Figure()

    user_predictions = get_user_history(user_id)
    prediction_value = None
    for prediction in user_predictions:
        if (prediction['country'] == country and
                prediction['age'] == age and
                prediction['sex'] == sex and
                prediction['year'] == year):
            prediction_value = prediction['prediction'] * 100
            print(f"Found prediction value: {prediction_value}")
            break

    if prediction_value is None:
        print("Prediction not found in user history.")
        return go.Figure()

    historical_data = df[
        (df['Country'] == country) &
        (df['Age'] == age) &
        (df['Sex'] == sex) &
        (df['Year'] <= year)
        ].sort_values(by='Year')

    years = historical_data['Year'].tolist()
    rates = (historical_data['Unemployment Rate (%)'] * 100).tolist()
    print(f"Historical Years: {years}")
    print(f"Historical Rates: {rates}")

    if year not in years:
        years.append(year)
        rates.append(prediction_value)
        print(f"Appended Prediction - Year: {year}, Rate: {prediction_value}")
    else:
        idx = years.index(year)
        rates[idx] = prediction_value
        print(f"Updated Year {year} with Prediction Rate: {prediction_value}")

    historical_years = [yr for yr in years if yr < 2024]
    historical_rates = [rate for yr, rate in zip(years, rates) if yr < 2024]

    prediction_years = [yr for yr in years if yr >= 2024]
    prediction_rates = [rate for yr, rate in zip(years, rates) if yr >= 2024]

    all_years = years
    all_rates = rates

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=all_years,
        y=all_rates,
        mode='lines',
        line=dict(color='#577564'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=historical_years,
        y=historical_rates,
        mode='markers',
        name='Historic data',
        marker=dict(
            size=10,
            color='#626058',
            symbol='circle'
        ),
        hoverinfo='text',
        hovertext=[
            f"<b>Year</b>: {yr}<br><b>Unemployment Rate</b>: {rate}%"
            for yr, rate in zip(historical_years, historical_rates)
        ]
    ))

    fig.add_trace(go.Scatter(
        x=prediction_years,
        y=prediction_rates,
        mode='markers',
        name='Prediction',
        marker=dict(
            size=10,
            color='red',
            symbol='circle'
        ),
        hoverinfo='text',
        hovertext=[
            f"<b>Year</b>: {yr}<br><b>Predicted Unemployment Rate</b>: {rate}%"
            for yr, rate in zip(prediction_years, prediction_rates)
        ]
    ))

    fig.update_layout(
        title=f"Unemployment Rate in {country}, Age: {age}, Sex: {sex}, for (2014-{year}) years",
        titlefont=dict(color='#626058', size=20),
        xaxis=dict(
            title='<b>Year</b>',
            color='#627254',
            showline=True,
            linewidth=2,
            tickangle=0,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title='<b>Unemployment Rate (%)</b>',
            color='#627254',
            showline=True,
            linewidth=2,
            tickfont=dict(size=12)
        ),
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#f9f9f9',
        hovermode='closest',
        autosize=True,
        legend=dict(
            orientation='h',
            x=0.5,
            xanchor='center',
            y=-0.2,
            traceorder='normal',
            font=dict(size=12)
        )
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
