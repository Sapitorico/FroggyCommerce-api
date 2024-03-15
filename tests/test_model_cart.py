import unittest

from . import BaseTestContext

# Models
from src.models.ModelProduct import ModelProduct
from src.models.ModelCart import ModelCart
from src.models.ModelUser import ModelUser

# Entities
from src.models.entities.Products import Product
from src.models.entities.Users import User


class TestModelCart(BaseTestContext):

    def register_user(self):
        user = User(full_name="Sapito Rico",
                    username="sapitorico",
                    email="example@gmail.com",
                    phone_number="12345678",
                    password=User.hash_password("12345678"))
        ModelUser.register(self.connection, user)
        data = User(email="example@gmail.com",
                    password="12345678")
        response = ModelUser.login(self.connection, data)
        return response[0].json['user']['id']

    def create_product(self):
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 10.99,
            "stock": 30,
            "category": "product category"
        }
        product = Product(**product_data)
        ModelProduct.create(self.connection, product)
        response = ModelProduct.get_products(self.connection)
        return response[0].json['products'][0]['id']

    def test_validate(self):
        cart_data = {
            "product_id": "1",
            "quantity": 1
        }
        response = ModelCart.validate(cart_data)
        self.assertIsNone(response)

    def test_validate_emty_data(self):
        cart_data = {}
        response = ModelCart.validate(cart_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "No data provided"})
        self.assertEqual(response[1], 400)

    def test_validate_missing_product_id(self):
        # Missing product_id
        cart_data = {"quantity": 1}
        response = ModelCart.validate(cart_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'product_id' field is required"})
        self.assertEqual(response[1], 400)

    def test_validate_invalid_product_id(self):
        # Invalid product_id (empty string)
        cart_data = {"product_id": "", "quantity": 1}
        response = ModelCart.validate(cart_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'product_id' field must be a non-empty string"})
        self.assertEqual(response[1], 400)

    def test_validate_missing_quantity(self):
        # Missing quantity
        cart_data = {"product_id": "1"}
        response = ModelCart.validate(cart_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'quantity' field is required"})
        self.assertEqual(response[1], 400)

    def test_validate_invalid_quantity(self):
        # Invalid quantity (not a number)
        cart_data = {"product_id": "1", "quantity": "invalid"}
        response = ModelCart.validate(cart_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'quantity' field must be a number and greater than 0"})
        self.assertEqual(response[1], 400)

    def test_validate_negative_quantity(self):
        # Negative quantity
        cart_data = {"product_id": "1", "quantity": -1}
        response = ModelCart.validate(cart_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'quantity' field must be a number and greater than 0"})
        self.assertEqual(response[1], 400)

    def test_validate_zero_quantity(self):
        # Zero quantity
        cart_data = {"product_id": "1", "quantity": 0}
        response = ModelCart.validate(cart_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'quantity' field must be a number and greater than 0"})
        self.assertEqual(response[1], 400)

    def test_validate_valid_data(self):
        # Valid data
        cart_data = {"product_id": "1", "quantity": 1}
        response = ModelCart.validate(cart_data)
        self.assertIsNone(response)

    def test_add_to_cart(self):
        user_id = self.register_user()
        prodcut_id = self.create_product()
        data = {
            "product_id": prodcut_id,
            "quantity": 1
        }
        response = ModelCart.add_to_cart(self.connection, user_id, data)
        self.assertEqual(response[0].json, {
                         "success": True, "message": "Product successfully added to cart"})
        self.assertEqual(response[1], 201)

    def test_add_to_cart_invalid(self):
        data = {
            "product_id": 1,
            "quantity": 1
        }
        response = ModelCart.add_to_cart(self.connection, 1, data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "Product not found"})
        self.assertEqual(response[1], 404)

    def test_get_cart(self):
        user_id = self.register_user()
        prodcut_id = self.create_product()
        data = {
            "product_id": prodcut_id,
            "quantity": 1
        }
        res = ModelCart.add_to_cart(self.connection, user_id, data)
        response = ModelCart.get_cart(self.connection, user_id)
        self.assertEqual(response[0].json['message'],
                         "Cart retrieved successfully")
        self.assertEqual(response[0].json['success'], True)
        self.assertEqual(response[1], 200)
        self.assertIn('id', response[0].json['cart'][0])
        self.assertIn('name', response[0].json['cart'][0])
        self.assertIn('price', response[0].json['cart'][0])
        self.assertIn('quantity', response[0].json['cart'][0])

    def test_get_cart_emty(self):
        user_id = self.register_user()
        response = ModelCart.get_cart(self.connection, user_id)
        self.assertEqual(response[0].json['message'],
                         "Cart retrieved successfully")
        self.assertEqual(response[0].json['success'], True)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json['cart'], [])

    def test_remove_to_cart(self):
        user_id = self.register_user()
        prodcut_id = self.create_product()
        data = {
            "product_id": prodcut_id,
            "quantity": 1
        }
        ModelCart.add_to_cart(self.connection, user_id, data)
        response = ModelCart.remove_to_cart(
            self.connection, user_id, prodcut_id)
        self.assertEqual(response[0].json, {
                         "success": True, "message": "Product successfully removed from cart"})
        self.assertEqual(response[1], 200)

    def test_remove_to_cart_invalid(self):
        user_id = self.register_user()
        response = ModelCart.remove_to_cart(self.connection, user_id, 1)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "Product is not in your cart"})
        self.assertEqual(response[1], 404)


if __name__ == '__main__':
    unittest.main()
