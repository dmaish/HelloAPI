import unittest
import json
from app import create_app, db
from app.models import User


class BorrowTestCase(unittest.TestCase):
    def setUp(self):
        """test variables and initialisation"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        # setting up the app's context
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

            admin = User(username="admin", email="admin.gmail.com",
                         password="adminpassword", is_admin=True)
            db.session.add(admin)
            db.session.commit()

        self.book = {
            "title": "The Da Vinci Code",
            "author": "Dan Brown",
            "category": "Mystery Thriller",
            "url": "http://www.bbhsfocus.com/2016/10/review-of-the-da-vinci-code-by-dan-brown/"
        }
        self.user_data = {
            "username": "admin",
            "email": "admin.gmail.com",
            "password": "adminpassword"
        }
        self.login_credentials = {
            "email": "mainadaniel81@gmail.com",
            "password": "bluestrokes"
        }

    def get_access_token(self, user):
        """registers and generates an access token for the user"""
        self.client.post("/api/auth/register", data=user)
        response_login = self.client.post("/api/auth/login", data=user)
        result = json.loads(response_login.data)
        return result["access_token"]

    def test_book_borrowing(self):
        """Testing if authenticated user can borrow a book"""
        access_token = self.get_access_token(self.user_data)
        new_book = self.client.post("/api/books",
                                    data=json.dumps(self.book),
                                    headers={
                                        'content-type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)
                                    })
        self.assertEqual(new_book.status_code, 201)

        response_borrow = self.client.post("/api/users/books/1",
                                           headers={'content-type': 'application/json',
                                                    'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response_borrow.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
