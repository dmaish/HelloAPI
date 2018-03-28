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
            "id": 4,
            "title": "The Da Vinci Code",
            "author": "Dan Brown",
            "category": "Mystery Thriller"
        }
        self.user_data={
            "username": "daniel",
            "email": "mainadaniel81@gmail.com",
            "password": "youllneverguess"
        }

    def test_new_book_creation(self):
        """Test f API can create a new book(POST request)"""
        post_res = self.client.post('/api/books/', data=self.book)
        self.assertEqual(post_res.status_code, 201)
        self.assertIn('The Da Vinci Code', str(post_res.data))

    def test_get_all_books(self):
        """Test if API can get all books"""
        get_res = self.client.get('/api/books/')
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('The Da Vinci Code', str(get_res.data))

    def test_get_book_by_id(self):
        """Test if book can be retrieved by id"""
        get_res = self.client.get('/api/books/{}'.format(self.book["title"]))
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('The Da Vinci Code', str(get_res.data))

    def test_can_edit_book(self):
        """Test if API can edit an existing book"""
        put_res = self.client.put('/api/books/The Da Vinci Code', data={'title': 'inferno'})
        self.assertEqual(put_res.status_code, 200)
        results = self.client.get('/api/books/The Da Vinci Code')
        self.assertIn('The Da Vinci Code', str(results.data))

    def test_book_deletion(self):
        """Test if API can delete an existing book.(DELETE request)"""
        post_res = self.client.post('/api/books/', data=self.book)
        self.assertEqual(post_res.status_code, 201)
        del_res = self.client.delete('/api/books/1')
        self.assertEqual(del_res.status_code, 404)

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.client().post('/api/auth/register', data=self.user_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "You registered successfully.")
        self.assertEqual(res.status_code, 201)

    def tearDown(self):
        self.app.app_context()


if __name__ == '__main__':
    unittest.main()
