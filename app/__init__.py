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
            book = {"id": json_res["id"], "title": json_res["title"], "author": json_res["author"],
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
    @app.route('/api/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def get_edit_remove_book(id):
        """Retrieve ,Edit or Remove book using Id"""

        # get specific book using title
        if request.method == 'GET':
            response = jsonify(book_model.book_specific(id))
            response.status_code = 200
            return response

        # edit a specific book using title
        elif request.method == 'PUT':
            json_res = request.get_json(force=True)
            book_update = {
                "id": json_res["id"],
                "title": json_res["title"],
                "author": json_res["author"],
                "category": json_res["category"],
                "url": json_res["url"]
            }
            response = jsonify(book_model.book_update(id, book_update))
            response.status_code = 200
            return response

        elif request.method == 'DELETE':
            book_model.book_delete(id)
            return "message: {} deleted successfully".format(id), 200

        @app.route('/api/auth/register/', method=['POST'])
        def register():
            user_obj = User()
            test_user=user_obj.test_dict
            user_obj.registration(test_user["username"],
                                  test_user["email"],
                                  test_user["password"])
            response = {
                'message': 'You registered successfully. Please log in.'
            }

            return jsonify(response), 201

        @app.route('/api/auth/login', methods=['POST'])
        def login():
            return ''

        @app.route('/api/users/books/<bookId', methods=['POST'])
        def borrow_book():
            return ''

        @app.route('/api/auth/logout/', methods=['POST'])
        def logout():
            return ''


    return app
