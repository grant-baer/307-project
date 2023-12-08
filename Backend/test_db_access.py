import unittest
from unittest.mock import MagicMock, patch
from db_access import *


class TestDBAccess(unittest.TestCase):
    def test_db_connect(self):
        assert db_connect() == 1

    # CHECK create_user

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

    # TEST check_user

    def test_check_user_existing_username(self):
        db_connect()
        data = {"username": "DONT_DELETE_CASEY"}
        response = check_user(data)
        assert response.status_code == 401 and "Username" in response.message

    def test_check_user_existing_email(self):
        db_connect()
        data = {"username": "", "email": "DONT@DONT.DONT"}
        response = check_user(data)
        assert response.status_code == 401 and "Email" in response.message

    def test_check_user_unique(self):
        data = {"username": "", "email": ""}
        response = check_user(data)
        assert response.status_code == 200

    # TEST get_user
    @patch("db_access.User")
    def test_get_user_found(self, MockUser):
        # Mocking the User.objects method to return a user
        mock_user_instance = MockUser.objects.return_value
        mock_user_instance.first.return_value = MagicMock()

        data = {"username": "test_user"}
        response = get_user(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.message, "User found.")

    # TEST create_image (3)

    @patch("db_access.User")
    @patch("db_access.Image")
    def test_create_image_success(self, MockImage, MockUser):
        # Mocking the save method of the Image model
        db_connect()
        username = {"username": "DONT_DELETE_CASEY"}
        user = get_user(username)

        image_data = {
            "creator": "6570d488e712f054d18ebebc",
            "prompt": "test_password",
            "data": "example_data",
        }
        response = create_image(image_data)
        assert response.status_code == 201

    @patch("db_access.User")
    def test_create_image_failure(self, MockUser):
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

    @patch("db_access.Image")
    @patch("db_access.User")
    def test_create_image_creator_not_exist(self, MockUser, MockImage):
        # Mocking the User.objects.get method to raise DoesNotExist
        mock_user_instance = MockUser.objects.get
        mock_user_instance.side_effect = DoesNotExist

        image_data = {
            "creator": "",  # username will never exist
            "prompt": "test_prompt",
            "data": "test_data",
        }

        response = create_image(image_data)

        # Assert that the response status code is 404 and the message matches
        # the expected message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.message, "Creator user does not exist.")

    @patch("db_access.Image")
    @patch("db_access.User")
    def test_create_image_internal_error(self, MockUser, MockImage):
        # Mocking the User.objects.get method to raise DoesNotExist
        mock_user_instance = MockUser.objects.get
        mock_user_instance.side_effect = Exception("test exception")

        image_data = {
            "creator": "",  # username will never exist
            "prompt": "test_prompt",
            "data": "test_data",
        }

        response = create_image(image_data)

        # Assert that the response status code is 404 and the message matches
        # the expected message
        self.assertEqual(response.status_code, 500)

    # TEST get_portfolio (3)


if __name__ == "__main__":
    unittest.main()
