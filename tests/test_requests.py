# third party imports
import unittest
import json

# local imports
from app.models import User
from app import create_app, db


class BookListApiTestcase(unittest.TestCase):
    """class representing the test case"""

    def setUp(self):
        """test variables and initialisation"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        # setting up the app's context
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
            admin = User(username="admin", email="admin@gmail.com",
                         password="adminpassword", is_admin=True)
            db.session.add(admin)
            db.session.commit()

        self.book = {
            "title": "The Da Vinci Code",
            "author": "Dan Brown",
            "category": "Mystery Thriller",
            "url": "http://www.bbhsfocus.com/2016/10/review-of-the-da-vinci-code-by-dan-brown/"
        }
        self.book2 = {
            "title": "Inferno",
            "author": "Dan Brown",
            "category": "Mystery Thriller",
            "url": "http://www.bbhsfocus.com/2016/10/review-of-the-da-vinci-code-by-dan-brown/"
        }
        self.user_data = {
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "adminpassword"
        }
        self.login_credentials = {
            "email": "admin@gmail.com",
            "password": "adminpassword"
        }

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def get_access_token(self, user):
        """registers and generates an access token for the user"""
        self.client.post("/api/auth/register", data=user)
        response_login = self.client.post("/api/auth/login", data=user)
        result = json.loads(response_login.data)
        return result["access_token"]

    def test_new_book_creation(self):
        """Test f API can create a new book(POST request)"""
        access_token = self.get_access_token(self.user_data)
        post_res = self.client.post('/api/books', data=json.dumps(self.book), headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(post_res.status_code, 201)
        self.assertIn('The Da Vinci Code', str(post_res.data))

    def test_get_all_books(self):
        """Test if API can get all books"""
        access_token = self.get_access_token(self.user_data)
        post_res = self.client.post('/api/books', data=json.dumps(self.book), headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(post_res.status_code, 201)
        get_res = self.client.get('/api/books', headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('The Da Vinci Code', str(get_res.data))

    def test_get_book_by_id(self):
        """Test if book can be retrieved by id"""
        access_token = self.get_access_token(self.user_data)
        post_res = self.client.post('/api/books', data=json.dumps(self.book), headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(post_res.status_code, 201)
        get_res = self.client.get('/api/books/1', headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('The Da Vinci Code', str(get_res.data))

    def test_can_edit_book(self):
        """Test if API can edit an existing book"""
        access_token = self.get_access_token(self.user_data)
        post_res = self.client.post('/api/books', data=json.dumps(self.book), headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(post_res.status_code, 201)
        put_res = self.client.put('/api/books/1', data=json.dumps(self.book2), headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(put_res.status_code, 200)
        results = self.client.get('/api/books/1', headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertIn('Inferno', str(results.data))

    def test_book_deletion(self):
        """Test if API can delete an existing book.(DELETE request)"""
        access_token = self.get_access_token(self.user_data)
        post_res = self.client.post('/api/books', data=json.dumps(self.book), headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(post_res.status_code, 201)
        del_res = self.client.delete('/api/books/1', headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
        self.assertEqual(del_res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
