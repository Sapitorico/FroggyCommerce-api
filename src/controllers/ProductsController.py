from flask import jsonify

# Models
from src.models.ProductsModel import ProductsModel


class ProductsController():
    """
    Controller class for managing products in an e-commerce system.
    """

    @classmethod
    def create_products(cls, data):
        """
        Create a new product.
        """
        product = ProductsModel(name=data['name'], description=data['description'], price=data['price'], stock=data['stock'],
                                category=data['category'], images=data['images'])
        response = product.create()
        return response

    @classmethod
    def get_product_by_id(cls, id):
        """
        Get a product by its ID.
        """
        product, response = ProductsModel.get_by_id(id)
        if product:
            product = ProductsModel(id=product[0], name=product[1], description=product[2], price=product[3], stock=product[4],
                                    category=product[5], created_at=product[6], updated_at=product[7], images=product[8]).to_dict()
        return product, response

    @classmethod
    def update_product(cls, id, data):
        """
        Update a product.
        """
        product = ProductsModel(id=id, name=data['name'], description=data['description'], price=data['price'],
                                stock=data['stock'], category=data['category'], images=data['images'])
        response = product.update()
        return response

    @classmethod
    def pagination(cls, page, per_page, category, name):
        """
        Retrieve a paginated list of products.
        """
        products, total_pages, response = ProductsModel.pagination(
            page, per_page, category, name)
        if products:
            products = [ProductsModel(id=product[0], name=product[1], description=product[2], category=product[3], price=product[4],
                                      stock=product[5], images=product[6], created_at=product[7], updated_at=product[8]).to_dict() for product in products]
        return products, total_pages, response
