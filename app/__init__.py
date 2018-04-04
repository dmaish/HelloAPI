# third party imports
from flask import Flask, jsonify
from flask_api import FlaskAPI
from flask import request, jsonify, abort
# local imports
from config import app_config
from app.models import *
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


# the following method accepts environment variable as its variable
def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    jwt = JWTManager(app)
    # importation of models should be here wen it comes to database

    @app.route('/api/books/', methods=['GET', 'POST'])
    @jwt_required
    def list_books_new_book():

        if request.method == 'POST':

            json_res = request.get_json(force=True)

            # creating new book instance
            new_book = BooksModel()
            new_book.id = json_res["id"]
            new_book.title = json_res["title"]
            new_book.author = json_res["author"]
            new_book.category = json_res["category"]
            new_book.url = json_res["url"]
            new_book.book_add()

            response = jsonify({"books": BooksModel.book_all()})
            response.status_code = 201
            return response

        # listing all available books in the library
        elif request.method == 'GET':

            response = jsonify({"books": BooksModel.book_all()})
            response.status_code = 200
            return response

    # getting a specific book using the title as primary key
    @app.route('/api/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required
    def get_edit_remove_book(id):
        """Retrieve ,Edit or Remove book using Id"""

        # get specific book using id
        if request.method == 'GET':
            book = BooksModel.book_specific(id)
            response = jsonify({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "url": book.url
            })
            response.status_code = 200
            return response

        # edit a specific book using title
        elif request.method == 'PUT':
            json_res = request.get_json(force=True)
            book_update = BooksModel()
            book_update.id = json_res["id"]
            book_update.title = json_res["title"]
            book_update.author = json_res["author"]
            book_update.category = json_res["category"]
            book_update.url = json_res["url"]

            # get edited book
            edited_book = BooksModel.update(id, book_update)
            response = jsonify({
                "id": edited_book.id,
                "title": edited_book.title,
                "author": edited_book.author,
                "category": edited_book.category,
                "url": edited_book.url
            })
            response.status_code = 200
            return response
        elif request.method == 'DELETE':
            BooksModel.book_delete(id)
            return "message: {} deleted successfully".format(id), 404

    @app.route("/api/users/books/<int:id>", methods=["POST"])
    @jwt_required
    def borrow_book(id):
        """Retrieve a specific book and allow user to borrow"""
        # get details of book being borrowed
        book = BooksModel().book_specific(id)

        # get user borrowing book
        user_email = get_jwt_identity()
        user = User().get_by_email(user_email)

        response = {
            "user": user.username,
            "book_borrowed": book["title"]
        }
        # response.status_code = 200
        return jsonify(response), 200

    # importing the authentication blueprint and register it on the app
    from .auth import auth
    app.register_blueprint(auth)

    return app
