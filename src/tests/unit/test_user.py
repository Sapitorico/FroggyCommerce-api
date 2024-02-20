import unittest

# Entities
from src.models.entities.Users import User


class TestUser(unittest.TestCase):

    def test_hash_password(self):
        password = "12345678"
        hashed_password = User.hash_password(password)
        self.assertTrue(hashed_password)

    def test_check_password(self):
        password = "12345678"
        hashed_password = User.hash_password(password)
        self.assertTrue(User.check_password(hashed_password, password))


if __name__ == '__main__':
    unittest.main()
