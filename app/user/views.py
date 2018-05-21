from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify

# local imports
from . import user
from ..models import *
import logging


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
    """method to get unreturned books by logged in user"""
    books = []
    user_email = get_jwt_identity()
    current_user = User.get_user_by_email(user_email)
    unreturned_records = Borrow_Record.query.filter_by(user_borrowed=current_user.id,
                                                       return_flag=False).all()

    for each_record in unreturned_records:
        book = Book.query.filter_by(id=each_record.book_id).first()
        record = {"id": book.id,
                  "title": book.title,
                  "author": book.author,
                  "category": book.category,
                  "url": book.url}

        books.append(record)

    response = {
        "unreturned books": books
    }
    return jsonify(response), 200


@user.route("/api/users/books", methods=["GET"])
@jwt_required
def get_user_borrowing_history():
    """method to get the logged in user borrowing history"""
    history = []
    user_email = get_jwt_identity()
    current_user = User.get_user_by_email(user_email)
    records = Borrow_Record.query.filter_by(user_borrowed=current_user.id).all()

    for each_record in records:
        book = Book.query.filter_by(id=each_record.book_id).first()
        record = {"title": book.title,
                  "author": book.author,
                  "category": book.category,
                  "date_borrowed": "-",
                  "date_returned": "-",
                  "return_flag": each_record.return_flag}

        history.append(record)

    response = {
        "borrowing history": history
    }
    return jsonify(response), 200









