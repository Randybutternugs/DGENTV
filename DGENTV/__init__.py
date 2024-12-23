from flask import Flask
from .constants import SITE_SECRET

def create_app():
    app = Flask(__name__)

    #CHANGE THIS LATER
    app.config['SECRET_KEY'] = SITE_SECRET
    #CHANGE THIS LATER

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
