from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from app import db


class User(db.Model):
    """model class for creating a users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    borrow_records = db.relationship('Borrow_Record', backref='user', lazy='dynamic')

    @property
    def password(self):
        """property decorator replaces getters\setters"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """set password to a hashed password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, input_password):
        """method to check if user password matches hashed password"""
        return check_password_hash(self.password_hash, input_password)

    @staticmethod
    def get_user_by_email(email):
        """method to get a user through email if user is registered"""
        user = User.query.filter_by(email=email).first()
        return user

    def __repr__(self):
        return '<User:{}>'.format(self.username)


class Book(db.Model):
    """model class for creating books table"""
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), index=True, unique=True)
    category = db.Column(db.String(60), index=True)
    author = db.Column(db.String(60), index=True)
    url = db.Column(db.String(100))
    borrowed_flag = db.Column(db.Boolean, default=False)
    users = db.relationship('Borrow_Record', backref='book', lazy='dynamic')

    def __repr__(self):
        return '<Book:{}>'.format(self.title)


class Borrow_Record(db.Model):
    """model class for creating borrow_records table"""
    __tablename__ = 'borrow_records'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'),
                        nullable=False)
    user_borrowed = db.Column(db.Integer, db.ForeignKey('users.id'),
                              nullable=False)
    time_borrowed = db.Column(db.String(60))
    time_returned = db.Column(db.String(60))
    return_flag = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Borrow_Record:{}>'.format(self.book_borrowed, self.user_borrowed)
