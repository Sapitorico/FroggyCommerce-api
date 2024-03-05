import unittest

from tests import BaseTestContext

# Entities
from src.models.entities.Products import Product

# Models
from src.models.ModelProduct import ModelProduct


class TestModelProduct(BaseTestContext):

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

    def test_validate(self):
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 10.99,
            "stock": 30,
            "category": "product category"
        }
        response = ModelProduct.validate(product_data)
        self.assertIsNone(response)

    def test_validate_invalid(self):
        product_data = {
            "description": "product description",
            "price": 10.99,
            "stock": 30,
            "category": "product category"
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'name' field is required"})
        self.assertEqual(response[1], 400)

        # Test invalid price
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": "invalid",
            "stock": 30,
            "category": "product category"
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'price' field must be a number and greater than 0"})
        self.assertEqual(response[1], 400)

        # Test negative price
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": -10.99,
            "stock": 30,
            "category": "product category"
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'price' field must be a number and greater than 0"})
        self.assertEqual(response[1], 400)

        # Test invalid stock
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 10.99,
            "stock": "invalid",
            "category": "product category"
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'stock' field must be a number and greater than 0"})
        self.assertEqual(response[1], 400)

        # Test negative stock
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 10.99,
            "stock": -30,
            "category": "product category"
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'stock' field must be a number and greater than 0"})
        self.assertEqual(response[1], 400)

        # Test missing category
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 10.99,
            "stock": 30
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'category' field is required"})
        self.assertEqual(response[1], 400)

        # Test invalid category
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 10.99,
            "stock": 30,
            "category": 12345
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'category' field must be a non-empty string"})
        self.assertEqual(response[1], 400)

    def test_data_types(self):
        # Test invalid data types
        product_data = {
            "name": 12345,
            "description": 67890,
            "price": "invalid",
            "stock": "invalid",
            "category": 12345
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "'name' field must be a non-empty string"})
        self.assertEqual(response[1], 400)

    def test_optional_fields(self):
        # Test optional fields
        product_data = {
            "name": "product name",
            "price": 10.99,
            "stock": 30,
            "category": "product category"
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         'message': "'description' field is required", 'success': False})

    def test_edge_cases(self):
        # Test edge cases
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 0,
            "stock": 0,
            "category": ""
        }
        response = ModelProduct.validate(product_data)
        self.assertEqual(response[0].json, {
                         'message': "'price' field must be a number and greater than 0", 'success': False})

    def test_create_product(self):
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 10.99,
            "stock": 30,
            "category": "product category"
        }
        product = Product(**product_data)
        response = ModelProduct.create(self.connection, product)
        self.assertEqual(response[0].json, {
                         'message': 'Successfully created product', 'success': True})
        self.assertEqual(response[1], 201)

    def test_create_product_invalid(self):
        self.create_product()
        product_data = {
            "name": "product name",
            "description": "product description",
            "price": 10.99,
            "stock": 30,
            "category": "product category"
        }
        product = Product(**product_data)
        response = ModelProduct.create(self.connection, product)
        self.assertEqual(response[0].json, {
                         'message': 'Product already exists', 'success': False})
        self.assertEqual(response[1], 400)

    def test_get_products(self):
        self.create_product()
        response = ModelProduct.get_products(self.connection)
        self.assertEqual(response[0].json['message'],
                         "Products retrieved successfully")
        self.assertEqual(response[0].json['success'], True)
        self.assertIn('id', response[0].json['products'][0])
        self.assertIn('name', response[0].json['products'][0])
        self.assertIn('description', response[0].json['products'][0])
        self.assertIn('price', response[0].json['products'][0])
        self.assertIn('stock', response[0].json['products'][0])
        self.assertIn('category', response[0].json['products'][0])
        self.assertEqual(response[1], 200)

    def test_get_product_empty(self):
        response = ModelProduct.get_products(self.connection)
        self.assertEqual(response[0].json['message'],
                         "Products retrieved successfully")
        self.assertEqual(response[0].json['success'], True)
        self.assertEqual(response[0].json['products'], [])
        self.assertEqual(response[1], 200)

    def test_get_product_by_id(self):
        self.create_product()
        res = ModelProduct.get_products(self.connection)
        id = res[0].json['products'][0]['id']
        response = ModelProduct.get_product_by_id(self.connection, id)
        self.assertEqual(response[0].json['message'],
                         "Product retrieved successfully")
        self.assertEqual(response[0].json['success'], True)
        self.assertIn('id', response[0].json['product'])
        self.assertIn('name', response[0].json['product'])
        self.assertIn('description', response[0].json['product'])
        self.assertIn('price', response[0].json['product'])
        self.assertIn('stock', response[0].json['product'])
        self.assertIn('category', response[0].json['product'])
        self.assertEqual(response[1], 200)

    def test_get_product_by_id_invalid(self):
        response = ModelProduct.get_product_by_id(self.connection, 1)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "Product not found"})
        self.assertEqual(response[1], 404)

    def test_update_prodcut(self):
        self.create_product()
        res = ModelProduct.get_products(self.connection)
        id = res[0].json['products'][0]['id']
        name = res[0].json['products'][0]['name']
        description = res[0].json['products'][0]['description']
        price = res[0].json['products'][0]['price']
        stock = res[0].json['products'][0]['stock']
        category = res[0].json['products'][0]['category']
        response = ModelProduct.update_product(self.connection, id, {
                                               "name": "new name", "description": "new description", "price": 20.99, "stock": 40, "category": "new category"})
        self.assertEqual(response[0].json, {
                         "success": True, "message": "Product successfully upgraded"})
        self.assertEqual(response[1], 200)
        res = ModelProduct.get_products(self.connection)
        self.assertEqual(res[0].json['products'][0]['id'], id)
        self.assertNotEqual(res[0].json['products'][0]['name'], name)
        self.assertNotEqual(res[0].json['products'][0]
                            ['description'], description)
        self.assertNotEqual(res[0].json['products'][0]['price'], price)
        self.assertNotEqual(res[0].json['products'][0]['stock'], stock)
        self.assertNotEqual(res[0].json['products'][0]['category'], category)

    def test_update_prodcut_invalid(self):
        response = ModelProduct.update_product(self.connection, 1, {
                                               "name": "new name", "description": "new description", "price": 20.99, "stock": 40, "category": "new category"})
        self.assertEqual(response[0].json, {
                         "success": False, "message": "Product not found"})
        self.assertEqual(response[1], 404)

    def test_delete_product(self):
        self.create_product()
        res = ModelProduct.get_products(self.connection)
        id = res[0].json['products'][0]['id']
        response = ModelProduct.delete_product(self.connection, id)
        self.assertEqual(response[0].json, {
                         "success": True, "message": "Product successfully deleted"})
        self.assertEqual(response[1], 200)

    def test_delete_product_invalid(self):
        response = ModelProduct.delete_product(self.connection, 1)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "Product not found"})
        self.assertEqual(response[1], 404)


if __name__ == "__main__":
    unittest.main()
