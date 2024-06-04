from flask import jsonify

# Models
from src.models.CategoriesModel import CategoriesModel


class CategoriesController():

    @classmethod
    def get_categories(cls):
        response = CategoriesModel.get()
        if not response:
            return jsonify({"success": False, "message": "No categories found"}), 404
        categories = [CategoriesModel(
            id=categorie[0], name=categorie[1], image_url=categorie[2]).to_dict() for categorie in response]
        return jsonify({"success": True, "message": "Categories retrieved successfully", "categories": categories}), 200

    @classmethod
    def create_category(cls, data):
        validate = cls.validate(data)
        if validate:
            return validate
        category = CategoriesModel(
            id=None, name=data['name'], image_url=data['image_url'])
        result = category.create()
        if result == 'already_exists':
            return jsonify({"success": False, "message": "Category already exists"}), 409
        return jsonify({"success": True, "message": "Category created successfully"}), 200

    @classmethod
    def update_category(cls, id, data):
        validate = cls.validate(data)
        if validate:
            return validate
        category = CategoriesModel(
            id=id, name=data['name'], image_url=data['image_url'])
        result = category.update()
        if result == 'not_exists':
            return jsonify({"success": False, "message": "Category not found"}), 404
        elif result == 'already_exists':
            return jsonify({"success": False, "message": "Category already exists"}), 409
        return jsonify({"success": True, "message": "Category updated successfully"}), 200

    @staticmethod
    def validate(category):
        if not category:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if 'name' not in category:
            return jsonify({"success": False, "message": "'name' field is required"}), 400
        elif not isinstance(category['name'], str) or len(category['name']) == 0:
            return jsonify({"success": False, "message": "'name' field must be a non-empty string"}), 400

        if 'image_url' not in category:
            return jsonify({"success": False, "message": "'image_url' field is required"}), 400
        elif not isinstance(category['image_url'], str) or len(category['image_url']) == 0:
            return jsonify({"success": False, "message": "'image_url' field must be a non-empty url string"}), 400

        return None
