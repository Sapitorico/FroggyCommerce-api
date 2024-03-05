from datetime import datetime
import unittest

# Entities
from src.models.entities.Users import User


class TestUser(unittest.TestCase):

    def test_init_all_attributes(self):
        user_data = {
            'id': 1,
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'user_type': 'admin',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        user = User(**user_data)
        self.assertEqual(user.id, user_data['id'])
        self.assertEqual(user.full_name, user_data['full_name'])
        self.assertEqual(user.email, user_data['email'])
        self.assertEqual(user.password, user_data['password'])
        self.assertEqual(user.user_type, user_data['user_type'])
        self.assertEqual(user.created_at, user_data['created_at'])
        self.assertEqual(user.updated_at, user_data['updated_at'])

    def test_user_to_dict(self):
        user_data = {
            'id': 1,
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'user_type': 'admin',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        user = User(**user_data)
        user_dict = user.to_dict()
        self.assertEqual(user_dict['id'], user_data['id'])
        self.assertEqual(user_dict['full_name'], user_data['full_name'])
        self.assertEqual(user_dict['email'], user_data['email'])
        self.assertEqual(user_dict['user_type'], user_data['user_type'])
        self.assertEqual(
            user_dict['created_at'], user_data['created_at'].strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(
            user_dict['updated_at'], user_data['updated_at'].strftime('%Y-%m-%d %H:%M:%S'))

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
