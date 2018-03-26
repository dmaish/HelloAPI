# third parth imports
from flask import Flask, jsonify
from flask_api import FlaskAPI
from flask import request, jsonify, abort
# local imports
from config import app_config
from dummy_data import books


# the following method accepts environment variable as its variable
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    # importation of models should be here wen it comes to database

    @app.route('/api/books/', methods=['GET'])
    def get_all_books():

        all_books = []

        for book in books:
            book_details = {}
            book_details['id'] = book['id']
            book_details['title'] = book['title']
            book_details['author'] = book['author']
            book_details['category'] = book['category']
            all_books.append(book_details)
        response = jsonify(all_books)
        response.status_code = 200
        return response

    @app.route('/api/books/<int:id>', methods=['GET'])
    def get_book_by_id(id, **kwargs):
        """Retrieve book using Id"""
        for book in books:
            if book['id'] == id:
                response = jsonify(book)
                response.status_code = 200
        return response


    return app
