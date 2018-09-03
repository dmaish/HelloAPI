from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify, request

# local imports
from . import user
from ..models import *
import datetime


@user.route('/api/books', methods=["GET"])
def list_books():
    """method that allows users to list all books in the library"""
    books = []

    per_page = request.args.get('per_page', 20, type=int)
    page = request.args.get('page', 1, type=int)
    all_books = Book.query.paginate(per_page=per_page, page=page).items

    for each_book in all_books:
        book = {"id": each_book.id,
                "title": each_book.title,
                "author": each_book.author,
                "category": each_book.category,
                "borrowed_flag": each_book.borrowed_flag,
                "url": each_book.url}
        books.append(book)

    response = jsonify({"books": books})
    response.status_code = 200
    return response


@user.route("/api/users/books/<int:id>", methods=["POST"])
@jwt_required
def borrow_book(id):
    """Retrieve a specific book and allow user to borrow"""
    now = datetime.datetime.now()
    time = now.strftime("%B %d, %Y %H:%M")
    # get book being borrowed
    book = Book.query.filter_by(id=id).first()

    # get user borrowing book
    user_email = get_jwt_identity()
    borrower = User.get_user_by_email(user_email)

    # borrowing record
    if not book.borrowed_flag:
        record = Borrow_Record(user=borrower, book=book, time_borrowed=time)
        book.borrowed_flag = True
        db.session.add(record)
        db.session.commit()

        response = {
            "user borrowed": (User.query.filter_by(id=record.user_borrowed).first()).username,
            "book borrowed": (Book.query.filter_by(id=record.book_id).first()).title,
            "time borrowed": record.time_borrowed,
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
    """method to allow user to return a specific borrowed book"""
    now = datetime.datetime.now()
    time = now.strftime("%B %d, %Y %H:%M")

    user_email = get_jwt_identity()
    user = User.get_user_by_email(user_email)
    book = Book.query.filter_by(id=id).first()
    borrowing_record = Borrow_Record.query.filter_by(book_id=id, user_borrowed=user.id, return_flag=False).first()

    borrowing_record.return_flag = True
    borrowing_record.time_returned = time
    book.borrowed_flag = False
    db.session.add(borrowing_record)
    db.session.commit()
    response = {
        "message": "successfully returned",
        "time returned": borrowing_record.time_returned
    }
    return jsonify(response), 200


@user.route("/api/users/books", methods=["GET"])
@jwt_required
def get_user_borrowing_history():
    """method to get the logged in user borrowing history"""
    returned = request.args.get('returned', True)
    unreturned_records = []
    records = []

    if returned == 'false':
        books = []
        user_email = get_jwt_identity()
        # check if current user is admin.If so, show unreturned books for all users
        if User.check_if_user_is_admin():
            unreturned_records = Borrow_Record.query.filter_by(return_flag=False).all()
        else:
            current_user = User.get_user_by_email(user_email)
            unreturned_records = Borrow_Record.query.filter_by(user_borrowed=current_user.id,
                                                               return_flag=False).all()

        for each_record in unreturned_records:
            book = Book.query.filter_by(id=each_record.book_id).first()
            record = {"id": book.id,
                      "title": book.title,
                      "author": book.author,
                      "category": book.category,
                      "url": book.url,
                      "return_flag": each_record.return_flag}

            books.append(record)

        response = {
            "unreturned_books": books
        }
        return jsonify(response), 200
    else:
        history = []
        user_email = get_jwt_identity()
        # check if current user is admin.If so, show history for all users
        if User.check_if_user_is_admin():
            records = Borrow_Record.query.all()
        else:
            current_user = User.get_user_by_email(user_email)
            records = Borrow_Record.query.filter_by(user_borrowed=current_user.id).all()

        for each_record in records:
            book = Book.query.filter_by(id=each_record.book_id).first()
            record = {
                      "book id": book.id,
                      "title": book.title,
                      "author": book.author,
                      "category": book.category,
                      "time_borrowed": each_record.time_borrowed,
                      "time_returned": each_record.time_returned,
                      "return_flag": each_record.return_flag}

            history.append(record)

        response = {
            "borrowing_history": history
        }
        return jsonify(response), 200
