import unittest
import json
from app import create_app, db


class AuthenticateTestcase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        # setting up the app's context
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

        self.test_user = {
            "username": "testUser",
            "email": "testEmail@gmail.com",
            "password": "testpassword"
        }
        self.login_credentials = {
            "email": "testEmail@gmail.com",
            "password": "testpassword"
        }
        self.alternative_password = {
            "password": "alternative_password"
        }

    def get_access_token(self):
        """method to login and return the access token"""
        response = self.client.post("/api/auth/login", data=self.login_credentials)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        return result["access_token"]

    def test_registration(self):
        """Testing if user can register"""
        response = self.client.post("/api/auth/register", data=self.test_user)
        # getting the results returned in json format
        result = json.loads(response.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result["message"], "you registered successfully")
        self.assertEqual(response.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user can't register twice"""
        response = self.client.post("/api/auth/register", data=self.test_user)
        self.assertEqual(response.status_code, 201)
        second_response = self.client.post("/api/auth/register", data=self.test_user)
        self.assertEqual(second_response.status_code, 202)
        result = json.loads(second_response.data.decode())
        self.assertEqual(result["message"], "User already exists.Please login")

    def test_user_login(self):
        """Test if registered user can be logged in """
        register_response = self.client.post("/api/auth/register", data=self.test_user)
        self.assertEqual(register_response.status_code, 201)
        login_response = self.client.post("/api/auth/login", data=self.test_user)

        # get results after login attempt in json format
        result = json.loads(login_response.data.decode())
        # test the login response contains a success message
        self.assertEqual(result["message"], "You logged in successfully")
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(result["access_token"])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        # defining a dictionary to represent an unregistered user
        not_a_user = {
            "email": "not_a_user@example.com",
            "password": "nope"
        }
        response_login = self.client.post("/api/auth/login", data=not_a_user)
        result = json.loads(response_login.data.decode())
        self.assertEqual(response_login.status_code, 401)
        self.assertEqual(result["message"], "Invalid email or password, Please try again")

    # def test_password_reset(self):
    # TODo make sure to write test to reset password

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()

