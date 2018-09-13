# global imports
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import *

# local imports
from . import admin
from app import db
from ..models import User


@admin.route('/api/books', methods=['POST'])
@jwt_required
def add_book():
    """method to allow admin to add a new book in the library"""

    if request.method == 'POST':
        # checking if logged in user is admin
        if not User.check_if_user_is_admin():
            abort(403)

        json_res = request.get_json(force=True)
        title = json_res["title"]

        # check if book already exists
        if Book.query.filter_by(title=title).first():
            return jsonify("message: book already exists in the database")
        else:
            book = Book(title=title, author=json_res["author"],
                        category=request.json["category"], url=request.json["url"])

            db.session.add(book)
            db.session.commit()

            added_book = Book.query.filter_by(title=title).first()
            response = jsonify({
                                # "message": "success! '{}' added to the library".format(added_book.title),
                                "message": "success! book added to the library",
                                "book": {
                                            "id": added_book.id,
                                            "title": added_book.title,
                                            "author": added_book.author,
                                            "category": added_book.category,
                                            "url": added_book.url
                                            }
                                    })
            response.status_code = 201
            return response


# getting a specific book using the id as primary key
@admin.route('/api/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
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

        # checking if logged in user is admin
        if not User.check_if_user_is_admin():
            abort(403)

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

        response = jsonify({"message": "book edit successful",
                            "title": book.title,
                            "author": book.author,
                            "category": book.category,
                            "url": book.category})
        response.status_code = 200
        return response

    elif request.method == 'DELETE':
        # checking if logged in user is admin
        if not User.check_if_user_is_admin():
            abort(403)
        
        # check if book is available
        if Book.query.filter_by(id=id).first():
            # check if book is already borrowed before deleting
            if Borrow_Record.query.filter_by(book_id=id, return_flag=False).first():
                response = jsonify({"message": "you cannot delete book already borrowed"})
                response.status_code = 200
                return response

            else:
                db.session.delete(book)
                db.session.commit()
                response = jsonify({"message": "{} deleted successfully".format(id)})
                response.status_code = 200
                return response
        else:
            response = jsonify({"message": "book not available in the library"})
            response.status_code = 200
            return response
