# third parth imports
from flask import Flask, jsonify
from flask_api import FlaskAPI

# local imports
from config import app_config


# the following method accepts environment variable as its variable
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')

    return app
