import unittest
import json
from app import create_app
from app import models

class Authenticate(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.user = {
            "username": "testUser",
            "email": "testEmail@gmail.com",
            "password": "testpassword"
        }

    def tearDown(self):
        models

    def test_registration(self):
        """testing if new user can register"""
        user_registration = self.register_user(self.user)
        self.assertEqual(user_registration.status_code, 201)

