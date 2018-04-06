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

    # registering the authentication and endpoints blueprints
    from .auth import auth
    app.register_blueprint(auth)
    from .endpoints import endpoints
    app.register_blueprint(endpoints)

    return app
