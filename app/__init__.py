# third party imports
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy


# local imports
from config import app_config
from app.old_models import *
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


# the following method accepts environment variable as its variable
def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    jwt = JWTManager(app)

    # importing the authentication and admin blueprints and register them on the app
    from .auth import auth
    app.register_blueprint(auth)
    from .admin import admin
    app.register_blueprint(admin)

    return app
