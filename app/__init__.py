# third parth imports
from flask import Flask, jsonify
from flask_api import FlaskAPI
from flask import request, jsonify, abort
# local imports
from config import app_config
from models import *


# the following method accepts environment variable as its variable
def create_app(config_name):
    # adding a new book to the library
    book_model = BooksModel()

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    # importation of models should be here wen it comes to database

    @app.route('/api/books/', methods=['GET', 'POST'])
    def list_books_new_book():

        if request.method == 'POST':

            json_res = request.get_json(force=True)
            book = {"title": json_res["title"], "author": json_res["author"],
                    "category": request.json["url"]}
            book_model.book_add(book)
            response = jsonify({"books": BooksModel.all_books})
            response.status_code = 201
            return response

        # listing all available books in the library
        elif request.method == 'GET':

            response = jsonify({"books": book_model.book_all()})
            response.status_code = 200
            return response

    # getting a specific book using the title as primary key
    @app.route('/api/books/<string:book_title>', methods=['GET', 'PUT', 'DELETE'])
    def get_edit_remove_book(book_title):
        """Retrieve ,Edit or Remove book using Id"""

        # get specific book using title
        if request.method == 'GET':
            response = jsonify(book_model.book_specific(book_title))
            response.status_code = 200
            return response

        # edit a specific book using title
        elif request.method == 'PUT':
            json_res = request.get_json(force=True)
            book_update = {
            "title": json_res["title"],
            "author": json_res["author"],
            "category": json_res["category"],
            "url": json_res["url"]
            }
            response = jsonify(book_model.book_update(book_title, book_update))
            response.status_code = 200
            return response

        elif request.method == 'DELETE':
            book_model.book_delete(book_title)
            return "message: {} deleted successfully".format(book_title), 200

    return app
