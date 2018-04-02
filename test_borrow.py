import unittest
import json
from app import create_app
import app.models


class BorrowTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.context = self.app.app_context()
        self.client = self.app.test_client()
        self.book = {
            "id": 1,
            "title": "The Da Vinci Code",
            "author": "Dan Brown",
            "category": "Mystery Thriller",
            "url": "http://www.bbhsfocus.com/2016/10/review-of-the-da-vinci-code-by-dan-brown/"
        }
        self.user_data = {
            "username": "daniel",
            "email": "mainadaniel81@gmail.com",
            "password": "bluestrokes"
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
        new_book = self.client.post("/api/books/",
                                    data=json.dumps(self.book),
                                    headers={
                                        'content-type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)
                                    })
        self.assertEqual(new_book.status_code, 201)

        book = json.loads(new_book.data)
        response_borrow = self.client.post("/api/users/books/{}".format(self.book["id"]),
                                           headers={'content-type': 'application/json',
                                                    'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response_borrow.status_code, 200)

    def tearDown(self):
        self.app.context


if __name__ == '__main__':
    unittest.main()
