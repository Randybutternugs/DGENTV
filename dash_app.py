import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd

def init_dash(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dash/')
    dash_app.layout = html.Div([
        html.H1("Roobet Affiliate Stats Visualization"),
        dcc.Input(id='user-id-input', type='text', placeholder='User ID...', value='12345'),
        html.Button('Load Stats', id='load-button', n_clicks=0),
        dcc.Graph(id='stats-graph'),
        html.Div(id='error-message', style={'color': 'red'})
    ])

    @dash_app.callback(
        dash.dependencies.Output('stats-graph', 'figure'),
        dash.dependencies.Output('error-message', 'children'),
        dash.dependencies.Input('load-button', 'n_clicks'),
        dash.dependencies.State('user-id-input', 'value')
    )
    def update_graph(n_clicks, user_id):
        if n_clicks < 1:
            # No button pressed yet => return an empty figure
            return go.Figure(), ""

        try:
            resp = requests.get("http://localhost:5000/api/roobet-stats",
                                params={"userId": user_id})
            resp.raise_for_status()
            data = resp.json()

            # If we get an empty or invalid data structure, handle it:
            if not isinstance(data, list) or len(data) == 0:
                empty_fig = go.Figure()
                return empty_fig, "No valid data returned from Roobet"

            # Now transform 'data' into a DataFrame for Plotly Express
            # Example: if each item has 'username' and 'wagered'
            df = []
            for item in data:
                df.append({
                    "username": item.get('username', 'Unknown'),
                    "wagered": item.get('wagered', 0)
                })
            df = pd.DataFrame(df)
            fig = px.bar(df, x="username", y="wagered", title="Wagered Amounts")

            return fig, ""  # No error message

        except requests.exceptions.RequestException as e:
            # We got a 4xx or 5xx or network error
            empty_fig = go.Figure()
            return empty_fig, f"Error: {str(e)}"

    return dash_app
