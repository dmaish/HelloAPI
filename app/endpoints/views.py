# global imports
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.models import *
from . import endpoints


@endpoints.route('/api/books/', methods=['GET', 'POST'])
def create_new_and_get_all_books():
    """method to create a new book and to list all books"""

    if request.method == 'POST':

        json_res = request.get_json(force=True)
        # new_book.id = json_res["id"]
        title = json_res["title"]
        author = json_res["author"]
        category = json_res["category"]
        url = json_res["url"]

        # creating new book instance
        new_book = BooksModel(title, author, category, url)
        new_book.add_new_book()

        response = jsonify({"books": BooksModel.get_all_books()})
        response.status_code = 201
        return response

    # listing all available books in the library
    elif request.method == 'GET':

        response = {"books": BooksModel.get_all_books()}
        return jsonify(response), 200


# getting a specific book using the title as primary key
@endpoints.route('/api/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def edit_delete_and_get_specific_book(id):
    """Retrieve ,Edit or Remove book using Id"""

    # get specific book using id
    # make sure type is int
    if request.method == 'GET':
        book = BooksModel.book_specific(id)
        if book:
            response = {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "url": book.url
            }
            return jsonify(response), 200
        else:
            response = {
                "message": "there is no book with that id"
            }
            return jsonify(response), 404

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
        response = {
            "id": edited_book.id,
            "title": edited_book.title,
            "author": edited_book.author,
            "category": edited_book.category,
            "url": edited_book.url
        }
        return jsonify(response), 200
    elif request.method == 'DELETE':
        BooksModel.book_delete(id)
        return "message: {} deleted successfully".format(id), 404


@endpoints.route("/api/users/books/<int:id>", methods=["POST"])
@jwt_required
def borrow_a_book(id):
    """Retrieve a specific book and allow user to borrow"""
    # get details of book being borrowed
    book = BooksModel().book_specific(id)
    print book

    # get user borrowing book
    user_email = get_jwt_identity()
    user = UsersModel().get_by_email(user_email)

    response = {
        "user": user.username,
        "book_borrowed": book.title
    }
    return jsonify(response), 200