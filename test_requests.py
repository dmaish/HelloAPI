import unittest
import json
from app import create_app


class BookListApi(unittest.TestCase):
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
        self.user_data = {
            "username": "daniel",
            "email": "mainadaniel81@gmail.com",
            "password": "youllneverguess"
        }

    def test_new_book_creation(self):
        """Test f API can create a new book(POST request)"""
        post_res = self.client.post('/api/books/', data=json.dumps(self.book))
        self.assertEqual(post_res.status_code, 201)
        self.assertIn('The Da Vinci Code', str(post_res.data))

    def test_get_all_books(self):
        """Test if API can get all books"""
        post_res = self.client.post('/api/books/', data=json.dumps(self.book))
        self.assertEqual(post_res.status_code, 201)
        get_res = self.client.get('/api/books/')
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('The Da Vinci Code', str(get_res.data))

    def test_get_book_by_id(self):
        """Test if book can be retrieved by id"""
        get_res = self.client.get('/api/books/{}'.format(self.book["id"]))
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('The Da Vinci Code', str(get_res.data))

    def test_can_edit_book(self):
        """Test if API can edit an existing book"""
        post_res = self.client.post('/api/books/', data=json.dumps(self.book))
        self.assertEqual(post_res.status_code, 201)
        put_res = self.client.put('/api/books/{}'.format(self.book["id"]), data=json.dumps({'title': 'Inferno'}))
        self.assertEqual(put_res.status_code, 200)
        results = self.client.get('/api/books/{}'.format(self.book["id"]), )
        self.assertIn('Inferno', str(results.data))

    def test_book_deletion(self):
        """Test if API can delete an existing book.(DELETE request)"""
        post_res = self.client.post('/api/books/', data=json.dumps(self.book))
        self.assertEqual(post_res.status_code, 201)
        del_res = self.client.delete('/api/books/1')
        self.assertEqual(del_res.status_code, 404)

    def tearDown(self):
        self.app.app_context()


if __name__ == '__main__':
    unittest.main()
