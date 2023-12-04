import unittest

from db_access import *


class TestDBAccess(unittest.TestCase):
    def test_create_user(self):
        data = {
            "username": "test_user",
            "email": "test@gmail.com",
            "password": "test_password",
        }
        response = create_user(data)
        assert (
            response.status_code == 200
            and response.message == "User created successfully!"
        )

    def test_get_user(self):
        data = {"username": "existing_user"}
        response = get_user(data)
        assert (
            response.status_code == 401
            and response.message == "Username already exists. Choose another."
        )


if __name__ == "__main__":
    unittest.main()
