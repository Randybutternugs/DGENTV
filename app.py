# app.py
from flask import Flask, jsonify, request
import requests

def create_flask_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Example route: /api/roobet-stats
    @app.route('/api/roobet-stats', methods=['GET'])
    def fetch_roobet_stats():
        user_id = request.args.get('userId', '')
        if not user_id:
            return jsonify({"error": "userId is required"}), 400

        headers = {"Authorization": "Bearer YOUR_BEARER_TOKEN_HERE"}
        params = {"userId": user_id}

        url = "https://roobetconnect.com/affiliate/v2/stats"
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            return jsonify(data)
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == '__main__':
    # 1. Create the Flask app
    flask_app = create_flask_app()

    # 2. Import and initiate the Dash app, passing the Flask server
    from dash_app import init_dash
    dash_app = init_dash(flask_app)

    # 3. Run the combined server (Flask + Dash)
    #    By default, Dash is at /dash/ and Flask routes are at / (and /api/...).
    flask_app.run(debug=True, port=5000)
