import unittest
import json
from app import create_app
from app import models


class Authenticate(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        # setting up the app's context
        self.app_context = self.app.app_context()
        self.test_user = {
            "username": "testUser",
            "email": "testEmail@gmail.com",
            "password": "testpassword"
        }

    def test_registration(self):
        """Testing if user can register"""
        response = self.client.post("/api/auth/register", data=self.test_user)
        # getting the results returned in json format
        result = json.loads(response.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result["message"], "You registered successfully")
        self.assertEqual(response.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user can't register twice"""
        response = self.client.post("/api/auth/register", data=self.test_user)
        self.assertEqual(response.status_code, 201)
        second_response = self.client.post("/api/auth/register", data=self.test_user)
        self.assertEqual(second_response.status_code, 202)
        result = json.loads(second_response.data.decode())
        self.assertEqual(result["message"], "User already exists.Please login")

    def tearDown(self):
        self.app_context


if __name__ == '__main__':
    unittest.main()



