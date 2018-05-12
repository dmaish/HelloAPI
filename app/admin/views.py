# global imports
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Book

# local imports
from ..old_models import *
from . import admin
from app import db


@admin.route('/api/books/', methods=['GET', 'POST'])
# @jwt_required
def list_books_new_book():
    if request.method == 'POST':

        json_res = request.get_json(force=True)
        title = json_res["title"]
        book = Book(title=title, author=json_res["author"],
                    category=request.json["category"], url=request.json["url"])

        db.session.add(book)
        db.session.commit()

        added_book = Book.query.filter_by(title=title).first()
        response = jsonify({"title": added_book.title})
        response.status_code = 201
        return response

    # listing all available books in the library
    elif request.method == 'GET':
        books = []

        all_books = Book.query.all()

        for each_book in all_books:
            book = {"id": each_book.id,
                    "title": each_book.title,
                    "author": each_book.author,
                    "category": each_book.category,
                    "url": each_book.url}
            books.append(book)

        response = jsonify({"books": books})
        response.status_code = 200
        return response


# getting a specific book using the id as primary key
@admin.route('/api/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required
def get_edit_remove_book(id):
    """Retrieve ,Edit or Remove book using Id"""
    book = Book.query.filter_by(id=id).first()

    if request.method == 'GET':
        response = jsonify({"title": book.title,
                            "author": book.author,
                            "category": book.category,
                            "url": book.url})
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

        book.title = book_update["title"]
        book.author = book_update["author"]
        book.category = book_update["category"]
        book.url = book_update["url"]

        db.session.add(book)
        db.session.commit()

        response = jsonify({"title": book.title,
                            "author": book.author,
                            "category": book.category,
                            "url": book.category})
        response.status_code = 200
        return response

    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return "message: {} deleted successfully".format(id), 404


@admin.route("/api/users/books/<int:id>", methods=["POST"])
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
