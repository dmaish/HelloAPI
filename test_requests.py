import unittest
import json
from app import create_app, models


class BookListApiTestcase(unittest.TestCase):
    """class representing the test case"""

    def setUp(self):
        """test variables and initialisation"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.book = {
            "id": 1,
            "title": "The Da Vinci Code",
            "author": "Dan Brown",
            "category": "Mystery Thriller",
            "url": "http://www.bbhsfocus.com/2016/10/review-of-the-da-vinci-code-by-dan-brown/"
        }
        self.book2 = {
            "id": 1,
            "title": "Inferno",
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

    def tearDown(self):
        models.all_books

    def get_access_token(self, user):
        """registers and generates an access token for the user"""
        self.client.post("/api/auth/register", data=user)
        response_login = self.client.post("/api/auth/login", data=user)
        result = json.loads(response_login.data)
        return result["access_token"]

    def test_new_book_creation(self):
        """Test f API can create a new book(POST request)"""
        access_token = self.get_access_token(self.user_data)
        post_res = self.client.post('/api/books/', data=json.dumps(self.book), headers={
                                        'content-type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)
                                    })
        self.assertEqual(post_res.status_code, 201)
        self.assertIn('The Da Vinci Code', str(post_res.data))

    def test_get_all_books(self):
        """Test if API can get all books"""
        access_token = self.get_access_token(self.user_data)
        post_res = self.client.post('/api/books/', data=json.dumps(self.book), headers={
                                        'content-type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)
                                    })
        self.assertEqual(post_res.status_code, 201)
        get_res = self.client.get('/api/books/', headers={
                                        'content-type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)
                                    })
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('The Da Vinci Code', str(get_res.data))

    def test_get_book_by_id(self):
        """Test if book can be retrieved by id"""
        access_token = self.get_access_token(self.user_data)
        get_res = self.client.get('/api/books/{}'.format(1), headers={
                                        'content-type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)
                                    })
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('The Da Vinci Code', str(get_res.data))

    # def test_can_edit_book(self):
    # TODO make sure edit this test per expectations
    #     """Test if API can edit an existing book"""
    #     access_token = self.get_access_token(self.user_data)
    #     post_res = self.client.post('/api/books/', data=json.dumps(self.book), headers={
    #                                     'content-type': 'application/json',
    #                                     'Authorization': 'Bearer {}'.format(access_token)
    #                                 })
    #     self.assertEqual(post_res.status_code, 201)
    #     put_res = self.client.put('/api/books/{}'.format(self.book["id"]), data=json.dumps(self.book), headers={
    #                                     'content-type': 'application/json',
    #                                     'Authorization': 'Bearer {}'.format(access_token)
    #                                 })
    #     self.assertEqual(put_res.status_code, 200)
    #     results = self.client.get('/api/books/{}'.format(self.book["id"]), headers={
    #                                     'content-type': 'application/json',
    #                                     'Authorization': 'Bearer {}'.format(access_token)
    #                                 })
    #     self.assertIn('Inferno', str(results.data))

    def test_book_deletion(self):
        """Test if API can delete an existing book.(DELETE request)"""
        access_token = self.get_access_token(self.user_data)
        post_res = self.client.post('/api/books/', data=json.dumps(self.book), headers={
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
