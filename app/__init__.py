# third party imports
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


# the following method accepts environment variable as its variable
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # JWTManager(app)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=600)
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    # importing the authentication, admin and user blueprints and register them on the app
    from .auth import auth
    app.register_blueprint(auth)
    from .admin import admin
    app.register_blueprint(admin)
    from .user import user
    app.register_blueprint(user)

    return app
