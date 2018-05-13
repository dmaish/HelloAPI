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
    user = User.get_user_by_email(user_email)

    # borrowing record
    record = Borrow_Record(user=user, book=book)
    db.session.add(record)
    db.session.commit()

    response = {
        "return flag": record.user_borrowed,
        "book_borrowed": record.book_id
    }
    return jsonify(response), 200