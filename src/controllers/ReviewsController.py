from flask import jsonify

# Models
from src.models.ReviewsModel import ReviewsModel


class ReviewsController():

    @classmethod
    def get_reviews(cls, user_id):
        results = ReviewsModel.get_by_user(user_id)
        if not results:
            return jsonify({'success': False, 'message': 'No reviews found'}), 404
        reviews = [ReviewsModel(id=review[0], product_id=review[1],
                                product_name=review[2], image_url=review[3], rating=review[4]).to_dict()
                   for review in results if review[0]]
        products_without_review = [ReviewsModel(product_id=product[1],
                                                product_name=product[2], image_url=product[3]).to_dict()
                                   for product in results if not product[0]]
        return jsonify({'success': True, 'message': 'Reviews retrieved successfully',
                        'reviews': reviews, 'products_without_review': products_without_review}), 200

    @classmethod
    def create_review(cls, user_id, product_id, data):
        validate = cls.validate(data)
        if validate:
            return validate
        review = ReviewsModel(product_id=product_id, user_id=user_id,
                              rating=data['rating'], review=data['review'])
        result = review.create()
        if result == 'not_found':
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        if result == 'already_exists':
            return jsonify({'success': False, 'message': 'Review already exists'}), 400
        if result == 'success':
            return jsonify({'success': True, 'message': 'Review created successfully'}), 201
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

    @classmethod
    def get_review(cls, user_id, review_id):
        result = ReviewsModel.get(user_id, review_id)
        if not result:
            return jsonify({'success': False, 'message': 'Review not found'}), 400
        review = ReviewsModel(id=result[0], product_name=result[1], image_url=result[2], rating=result[3],
                              review=result[4]).to_dict()
        return jsonify({'success': True, 'message': 'Review retrieved successfully', 'review': review}), 200

    @classmethod
    def update_review(cls, user_id, review_id, data):
        validate = cls.validate(data)
        if validate:
            return validate
        review = ReviewsModel(id=review_id, user_id=user_id,
                              rating=data['rating'], review=data['review'])
        result = review.update()
        if not result:
            return jsonify({'success': False, 'message': 'Review not found'}), 404
        return jsonify({'success': True, 'message': 'Review updated successfully'}), 200

    @classmethod
    def get_reviews_by_product(cls, product_id):
        result = ReviewsModel.get_by_product(product_id)
        if not result:
            return jsonify({'success': False, 'message': 'Reviews not found'}), 404
        reviews = [ReviewsModel(id=review[0], rating=review[1], review=review[2], username=review[3],
                                created_at=review[4], updated_at=review[5]).to_dict()
                   for review in result]
        return jsonify({'success': True, 'message': 'Reviews retrieved successfully', 'reviews': reviews}), 200

    @staticmethod
    def validate(data):

        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        if 'rating' not in data:
            return jsonify({'success': False, 'message': '\'rating\' field requiered'}), 400
        elif not isinstance(data['rating'], int) or isinstance(data['rating'], bool) or data['rating'] <= 0 or data['rating'] > 5:
            return jsonify({'success': False, 'message': '\'rating\' field must be a number between 1 and 5'}), 400
        if 'review' not in data:
            return jsonify({'success': False, 'message': '\'review\' field requiered'}), 400
        elif not isinstance(data['review'], str) or len(data['review']) <= 0:
            return jsonify({'success': False, 'message': '\'review\' field must be a non-empty string'}), 400
        return None
