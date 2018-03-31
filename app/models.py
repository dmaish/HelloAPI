import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort, current_app
import datetime

all_users = []  # list containing all users in the library
borrowed_books = []  # list containing id of books borrowed and username who borrowed


class BooksModel:

    all_books = []

    def __init__(self):
        pass

    def book_add(self, book):
        """ method to add book dictionaries to the books list"""
        self.all_books.append(book)

    def book_all(self):
        """method returns all books"""
        return self.all_books

    def book_specific(self, id):
        """method returns specific book according to book id"""
        for each_book in self.all_books:
            if each_book["id"] == id:
                return each_book

    # FINISH UP THIS CODE THAT REPLACES THE UPDATED BOOK WITH THE OLD BOOK IN THE all_books LIST
    def book_update(self, id, book_update):
        """method returns specific book according to book id"""
        old_book = None
        for each_book in self.all_books:
            if each_book["id"] == id:
                old_book = each_book
        # finding the index of the book with matching title
        for i, j in enumerate(self.all_books):
            if j == old_book:
                # editing the books list
                self.all_books[i] = book_update
        return self.all_books

    def book_delete(self, id):
        """method deletes specific book according to book id"""
        old_book = None
        for each_book in self.all_books:
            if each_book["id"] == id:
                old_book = each_book
        # finding the index of the book with matching title
        for i, j in enumerate(self.all_books):
            if j == old_book:
                del self.all_books[i]


class User:
    """This class defines the users model"""
    def __init__(self):
        self.username = None
        self.email = None
        self.password = None
        self.is_admin = False

    def password_set(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save_user(self):
        all_users.append(self)

    @staticmethod
    def get_by_email(email):
        for user in all_users:
            if user.email == email:
                return user
