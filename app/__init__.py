# third party imports
from flask_api import FlaskAPI
from flask_jwt_extended import JWTManager

# local imports
from config import app_config
from app.models import *


# the following method accepts environment variables as its variable
def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    jwt = JWTManager(app)
    # importation of models should be here wen it comes to database

    # importing the authentication blueprint and register it on the app
    from .auth import auth
    app.register_blueprint(auth)

    return app
