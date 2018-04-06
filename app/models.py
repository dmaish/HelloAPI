# global imports
from werkzeug.security import generate_password_hash, check_password_hash
from time import strftime, gmtime
from flask import jsonify

# all books in the library
all_books = []
# all users
all_users = []
# all books borrowed
borrowed_books = []


class BooksModel:
    book_id = 1
    """class facilitating storing and manipulation of books"""
    def __init__(self, title, author, category, url):
        self.id = BooksModel.book_id
        self.title = title
        self.author = author
        self.category = category
        self.url = url
        BooksModel.book_id += 1

    def add_new_book(self):
        """ method to add book dictionaries to the books list"""
        all_books.append(self)

    @staticmethod
    def get_all_books():
        """method returns all books in json form"""
        books = []
        for each_book in all_books:
            book = {
                "id": each_book.id,
                "title": each_book.title,
                "author": each_book.author,
                "category": each_book.category,
                "url": each_book.url
            }
            books.append(book)
        return books

    @staticmethod
    def get_specific_book(id):
        """method returns specific book according to book id"""
        for book in all_books:
            if book.id == id:
                return book

    # FINISH UP THIS CODE THAT REPLACES THE UPDATED BOOK WITH THE OLD BOOK IN THE all_books LIST
    @staticmethod
    def update_specific_book(id, book_update):
        """method returns specific book according to book id"""
        edited_book = None
        for index, book in enumerate(all_books):
            if book.id == id:
                all_books[index] = book_update
                edited_book = all_books[index]

        return edited_book

    @staticmethod
    def delete_specific_books(id):
        """method deletes specific book according to book id"""
        for index, book in enumerate(all_books):
            if book.id == id:
                del all_books[index]


class UsersModel:
    """class facilitating storing and manipulation of users"""
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.books_by_particular_user = []

    def password_set(self, password):
        """hashes a users password before storage"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """validates if password is correct"""
        return check_password_hash(self.password, password)

    def save_user(self):
        """saves users and their data"""
        all_users.append(self)

    def user_book_borrow(self, id):
        """creates borrowing records after user borrows a record"""
        book = BooksModel.book_specific(id)
        self.books_by_particular_user.append(book)
        # appending to the borrowed books record
        borrow_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        borrowing_record = BorrowingRecord(book, book["title"], borrow_time, self)
        borrowed_books.append(borrowing_record)

    @staticmethod
    def get_by_email(email):
        """gets a specific user using the email"""
        for user in all_users:
            if user.email == email:
                return user

    @staticmethod
    def response_field_is_empty():
        response = {
            "message": "fill in all fields before submitting"
        }
        return jsonify(response), 409


class BorrowingRecord:
    """class facilitating in storage of book borrowing records and their manipulation"""
    def __init__(self, title, borrow_time, user):
        self.title = title
        self.borrow_time = borrow_time,
        self.user = user


class Blacklist:
    """this class stores revoked json web tokens"""
    def __init__(self):
        self.blacklist = []




















