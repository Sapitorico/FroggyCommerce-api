from flask import jsonify

# Models
from src.models.CategoriesModel import CategoriesModel


class CategoriesController():

    @classmethod
    def get_categories(cls):
        """
        Get all categories.
        """
        categories, response = CategoriesModel.get()
        if categories:
            categories = [CategoriesModel(
                id=category[0], name=category[1], image_url=category[2]).to_dict() for category in categories]
        return categories, response

    @classmethod
    def create_category(cls, data):
        """
        Create a new category.
        """
        category = CategoriesModel(
            name=data['name'], image_url=data['image_url'])
        result = category.create()
        return result

    @classmethod
    def update_category(cls, id, data):
        """
        Update an existing category.
        """
        category = CategoriesModel(
            id=id, name=data['name'], image_url=data['image_url'])
        result = category.update()
        return result
