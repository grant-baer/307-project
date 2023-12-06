import unittest
from unittest.mock import MagicMock, patch
import coverage
from db_access import *


class TestDBAccess(unittest.TestCase):
    def test_db_connect(self):
        assert db_connect() == 1

    @patch("db_access.User")
    def test_create_user_success(self, MockUser):
        # Mocking the save method of the User model
        data = {
            "username": "test_user",
            "password": "test_password",
            "email": "test@example.com",
        }
        response = create_user(data)
        assert response.status_code == 201

    @patch("db_access.User")
    def test_create_user_failure(self, MockUser):
        # Mocking the save method of the User model
        mock_user_instance = MockUser.return_value
        mock_user_instance.save.side_effect = Exception("test exception")

        data = {
            "username": "test_user",
            "password": "test_password",
            "email": "test@example.com",
        }
        response = create_user(data)
        assert response.status_code == 500

    def test_check_user_existing_username(self):
        db_connect()
        data = {"username": "existing_user"}
        response = check_user(data)
        assert response.status_code == 401 and "Username" in response.message

    def test_check_user_existing_email(self):
        db_connect()
        data = {"username": "", "email": "existing_user@gmail.com"}
        response = check_user(data)
        assert response.status_code == 401 and "Email" in response.message

    def test_check_user_unique(self):
        data = {"username": "", "email": ""}
        response = check_user(data)
        assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()
