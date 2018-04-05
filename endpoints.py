# third party imports
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
import app
from app.models import *


@app.route('/api/books/', methods=['GET', 'POST'])
def create_new_and_get_all_books():
    """method to create a new book and to list all books"""

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

        response = jsonify({"books": BooksModel.get_specific_book(new_book.id)})
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
def edit_delete_and_get_specific_book(id):
    """Retrieve ,Edit or Remove book using Id"""

    # get specific book using id
    # make sure type is int
    if request.method == 'GET':
        book = BooksModel.book_specific(id)
        if book:
            response = jsonify({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "url": book.url
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                "message": "there is no book with that id"
            })
            response.status_code = 404
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
def borrow_a_book(id):
    """Retrieve a specific book and allow user to borrow"""
    # get details of book being borrowed
    book = BooksModel().book_specific(id)
    print book

    # get user borrowing book
    user_email = get_jwt_identity()
    user = User().get_by_email(user_email)

    response = {
        "user": user.username,
        "book_borrowed": book.title
    }
    # response.status_code = 200
    return jsonify(response), 200