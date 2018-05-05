# global imports
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.old_models import *
from . import endpoints


@endpoints.route('/api/books/', methods=['GET', 'POST'])
# @jwt_required
def list_books_new_book():
    book_model = BooksModel()
    if request.method == 'POST':

        json_res = request.get_json(force=True)
        book = {"id": json_res["id"], "title": json_res["title"], "author": json_res["author"],
                "category": request.json["category"], "url": request.json["url"]}
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
@endpoints.route('/api/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required
def get_edit_remove_book(id):
    """Retrieve ,Edit or Remove book using Id"""
    book_model = BooksModel()

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
        return "message: {} deleted successfully".format(id), 404


@endpoints.route("/api/users/books/<int:id>", methods=["POST"])
# @jwt_required
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
    return jsonify(response), 200
