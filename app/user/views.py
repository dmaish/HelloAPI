from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify

# local imports
from . import user
from ..models import *


@user.route("/api/users/books/<int:id>", methods=["POST"])
@jwt_required
def borrow_book(id):
    """Retrieve a specific book and allow user to borrow"""
    # get book being borrowed
    book = Book.query.filter_by(id=id).first()

    # get user borrowing book
    user_email = get_jwt_identity()
    borrower = User.get_user_by_email(user_email)

    # borrowing record
    if not book.borrowed_flag:
        record = Borrow_Record(user=borrower, book=book)
        book.borrowed_flag = True
        db.session.add(record)
        db.session.commit()

        response = {
            "user borrowed": record.user_borrowed,
            "book borrowed": record.book_id,
            "message": "book borrowing success"
        }
        return jsonify(response), 200

    else:
        response = {
            "message": "book not available for borrowing"
        }
        return jsonify(response), 404


@user.route("/api/users/books/<int:id>", methods=["PUT"])
@jwt_required
def return_book(id):
    user_email = get_jwt_identity()
    user = User.get_user_by_email(user_email)
    book = Book.query.filter_by(id=id).first()
    borrowing_record = Borrow_Record.query.filter_by(book_id=id,
                                                     user_borrowed=user.id,
                                                     return_flag=False).first()
    borrowing_record.return_flag = True
    book.borrowed_flag = False
    db.session.commit()
    response = {
        "message": "book successfully returned"
    }
    return jsonify(response), 200


@user.route("/api/users/books?returned=false", methods=["GET"])
@jwt_required
def get_books_not_returned_by_user():
    return jsonify(), 200


@user.route("/api/users/books/", methods=["GET"])
@jwt_required
def get_user_borrowing_history():
    return jsonify(), 200


















