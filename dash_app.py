# dash_app.py
import dash
from dash import dcc, html, Input, Output
import requests
import plotly.express as px

def init_dash(flask_app):
    # Pass in the Flask server to Dash
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash/'  # Dash will be served at /dash/
    )

    # Layout of your Dash app
    dash_app.layout = html.Div([
        html.H1("Roobet Affiliate Stats Visualization"),
        dcc.Input(
            id='user-id-input',
            type='text',
            placeholder='Enter User ID...',
            value='12345',
            style={'marginRight': '10px'}
        ),
        html.Button('Load Stats', id='load-button', n_clicks=0),
        html.Div(id='error-message', style={'color': 'red'}),
        dcc.Graph(id='stats-graph')
    ])

    # Define Dash callbacks
    @dash_app.callback(
        Output('stats-graph', 'figure'),
        Output('error-message', 'children'),
        Input('load-button', 'n_clicks'),
        Input('user-id-input', 'value'),
    )
    def update_graph(n_clicks, user_id):
        """Fetch data from our Flask backend and plot it."""
        if n_clicks < 1:
            # No button click yet; return empty figure
            fig = px.scatter(x=[], y=[])
            return fig, ""

        # Call the Flask endpoint we created in app.py
        url = "http://localhost:5000/api/roobet-stats"
        try:
            resp = requests.get(url, params={"userId": user_id})
            resp.raise_for_status()
            data = resp.json()

            if not isinstance(data, list) or len(data) == 0:
                fig = px.scatter(x=[], y=[])
                return fig, "No data or invalid response."

            # Example chart: Let's plot 'wagered' vs. 'username'
            df_data = []
            for item in data:
                df_data.append({
                    "username": item.get('username', 'Unknown'),
                    "wagered": item.get('wagered', 0)
                })

            fig = px.bar(df_data, x="username", y="wagered",
                         title="User Wagered Amount")
            return fig, ""
        except requests.exceptions.RequestException as e:
            # Network or other request errors
            fig = px.scatter(x=[], y=[])
            return fig, f"Request Error: {str(e)}"
        except Exception as e:
            fig = px.scatter(x=[], y=[])
            return fig, f"Unexpected Error: {str(e)}"

    return dash_app
