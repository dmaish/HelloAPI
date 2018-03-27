from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
import jwt


class BooksModel:

    all_books = [{"id": 1, "title": "The Da Vinci Code", "author": "Dan Brown", "category": "Mystery", "url": "https..."},
             {"id": 2, "title": "Almost Heaven", "author": "Judith McNaught", "category": "Romance", "url": "https..."},
             {"id": 3, "title": "The Juror", "author": "John Grisham", "category": "Drama", "url": "https..."}]

    def __init__(self):
        pass

    def book_add(self, book):
        """ method to add book dictionaries to the books list"""
        self.all_books.append(book)

    def book_all(self):
        "method returns all books"
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
            if each_book["title"] == id:
                old_book = each_book
        # finding the index of the book with matching title
        for i, j in enumerate(self.all_books):
            if j == old_book:
                del self.all_books[i]


class User:

    users_list = []

    def __init__(self):
        """initilizes the admin user"""
        admin = {"username": "admin",
                 "email": "admin.gmail.com",
                 "password": generate_password_hash("bluestrokes")}

        self.users_list.append(admin)

    # before the user is registered they're checked if they exist already using email
    def registration(self, username, email, password):
        if self.check_user_exists(email):
            abort()
        else:
            new_user = {"username": username,
                        "email": email,
                        "password": self.salt_password(password)
            }
            self.users_list.append(new_user)

    @staticmethod
    def salt_password(password):
        """set password to a hashed password"""
        return generate_password_hash(password)

    # check if user exists using email
    def check_user_exists(self,email):
        for users in self.users_list:
            if email == users["email"]:
                return True
            else:
                return False


















