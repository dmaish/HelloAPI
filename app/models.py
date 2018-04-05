from time import strftime, gmtime

from werkzeug.security import generate_password_hash, check_password_hash

# all books in the library
all_books = []
# all users
all_users = []
# all books borrowed
borrowed_books = []


class BooksModel:
    """class facilitating storing and manipulation of books"""
    def __init__(self):
        self.id = None
        self.title = None
        self.author = None
        self.category = None
        self.url = None

    def book_add(self):
        """ method to add book dictionaries to the books list"""
        all_books.append(self)

    @staticmethod
    def book_all():
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
    def update(id, book_update):
        """method returns specific book according to book id"""
        edited_book = None
        for index, book in enumerate(all_books):
            if book.id == id:
                all_books[index] = book_update
                edited_book = all_books[i]

        return edited_book

    @staticmethod
    def book_delete(id):
        """method deletes specific book according to book id"""
        for index, book in enumerate(all_books):
            if book.id == id:
                del all_books[index]


class User:
    """class facilitating storing and manipulation of users"""
    def __init__(self):
        self.username = None
        self.email = None
        self.password = None
        self.is_admin = False
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




















