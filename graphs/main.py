import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import requests

unemployment_data = pd.read_csv('df_long_with_coordinates.csv')

location1 = unemployment_data[['Country', 'latitude', 'longitude']]
list_locations = location1.set_index('Country')[['latitude', 'longitude']].T.to_dict('dict')

region = unemployment_data['Continent'].unique()
continent = unemployment_data['Continent'].unique()
sex_categories = ['Total', 'Male', 'Female']

app = dash.Dash(__name__)

import flask
from requests import Session

def check_user_registration():
    try:
        with Session() as session:
            if flask.has_request_context():
                cookie = flask.request.cookies.get('session')
                if cookie:
                    session.cookies.set('session', cookie)

            response = session.get("http://127.0.0.1:5000/api/user-history")

        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            # Неавторизований доступ
            return False
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking user registration: {e}")
        return False

def serve_layout():
    is_registered = check_user_registration()
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
                           marks={year: {'label': str(year), 'style': {'color': '#627254', 'font-size': '20px'}} for year in
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

    # Додайте останню секцію лише якщо користувач зареєстрований
    if is_registered:
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
                    html.P("Select predictions from your history (Country, Age, Sex):", className='fix_label', style={'color': '#627254', 'font-weight': 'bold'}),
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

def fetch_user_predictions():
    try:
        with Session() as session:
            if flask.has_request_context():
                cookie = flask.request.cookies.get('session')
                if cookie:
                    session.cookies.set('session', cookie)

            response = session.get("http://127.0.0.1:5000/api/user-history")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch user predictions. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user predictions: {e}")
        return []



@app.callback(Output('detailed_analysis_section', 'style'),
              [Input('w_year', 'value')])
def toggle_detailed_analysis_visibility(w_year):
    ctx = dash.callback_context
    if not ctx.triggered or not flask.has_request_context() or not flask.request.cookies.get('session'):
        return {'display': 'none'}
    return {'display': 'flex'}


def fetch_user_predictions():
    try:
        # Створення сесії для передачі cookie
        with Session() as session:
            # Передача сесійного cookie з Flask додатка
            if flask.has_request_context():
                cookie = flask.request.cookies.get('session')
                if cookie:
                    session.cookies.set('session', cookie)

            response = session.get("http://127.0.0.1:5000/api/user-history")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch user predictions. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user predictions: {e}")
        return []


@app.callback(Output('w_prediction', 'options'),
              [Input('w_year', 'value')])
def update_prediction_dropdown(w_year):
    user_predictions = fetch_user_predictions()
    # Фільтруємо країни, вік і стать, які були передбачені в обраному році
    predictions = [
        {
            'label': f"{prediction['country']}, {prediction['age']}, {prediction['sex']}",
            'value': f"{prediction['country']}|{prediction['age']}|{prediction['sex']}"
        }
        for prediction in user_predictions if prediction.get('year') == w_year
    ]
    if predictions:
        return predictions
    return [{'label': 'No predictions available', 'value': None}]


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
                marker=dict(color='#627254'),
                name='Unemployment Rate',
                hoverinfo='text',
                hovertext='<b>Country</b>: ' + grouped_data['Country'] + '<br>' +
                          '<b>Unemployment Rate</b>: ' + grouped_data['UnemploymentRate'].astype(str) + '<br>'
            ),
            go.Scatter(
                x=grouped_data['Country'],
                y=grouped_data['UnemploymentRate'],
                mode='lines+markers',
                line=dict(color='#627254', width=2),
                marker=dict(size=5, color='#627254'),
                name='Trend Line',
                hoverinfo='text',
                hovertext='<b>Country</b>: ' + grouped_data['Country'] + '<br>' +
                          '<b>Unemployment Rate</b>: ' + grouped_data['UnemploymentRate'].astype(str) + '<br>'
            )
        ],
        'layout': go.Layout(
            title='Unemployment Rate by Country up to ' + str(select_year),
            titlefont=dict(color='#627254', size=20),
            xaxis=dict(title='<b>Country</b>', color='#DDDDDD', showline=True, linewidth=2, tickangle=-45),
            yaxis=dict(title='<b>Unemployment Rate</b>', color='#DDDDDD', showline=True, linewidth=2),
            plot_bgcolor='#f9f9f9',
            paper_bgcolor='#f9f9f9',
            hovermode='closest'
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
