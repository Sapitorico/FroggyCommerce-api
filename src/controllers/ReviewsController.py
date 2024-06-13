# Models
from src.models.ReviewsModel import ReviewsModel


class ReviewsController():

    @classmethod
    def get_reviews(cls, user_id):
        """
        Get reviews by user ID.
        """
        results = ReviewsModel.get_by_user(user_id)
        if results is not None:
            reviews = [ReviewsModel(id=review[0], product_id=review[1],
                                    product_name=review[2], image_url=review[3], rating=review[4]).to_dict()
                       for review in results if review[0]]
            products_without_review = [ReviewsModel(product_id=product[1],
                                                    product_name=product[2], image_url=product[3]).to_dict()
                                       for product in results if not product[0]]
            return reviews, products_without_review
        return None, None

    @classmethod
    def create_review(cls, user_id, product_id, data):
        """
        Create a new review.
        """
        review = ReviewsModel(product_id=product_id, user_id=user_id,
                              rating=data['rating'], review=data['review'])
        result = review.create()
        return result

    @classmethod
    def get_review(cls, user_id, review_id):
        """
        Get a review by user ID and review ID.
        """
        result = ReviewsModel.get(user_id, review_id)
        if result is not None:
            review = ReviewsModel(id=result[0], product_name=result[1], image_url=result[2], rating=result[3],
                                  review=result[4]).to_dict()
            return review

    @classmethod
    def update_review(cls, user_id, review_id, data):
        """
        Update a review.
        """
        review = ReviewsModel(id=review_id, user_id=user_id,
                              rating=data['rating'], review=data['review'])
        result = review.update()
        return result

    @classmethod
    def get_reviews_by_product(cls, product_id):
        """
        Get reviews by product ID.
        """
        results = ReviewsModel.get_by_product(product_id)
        if results is not None:
            reviews = [ReviewsModel(id=review[0], rating=review[1], review=review[2], username=review[3],
                                    created_at=review[4], updated_at=review[5]).to_dict()
                       for review in results]
            return reviews
