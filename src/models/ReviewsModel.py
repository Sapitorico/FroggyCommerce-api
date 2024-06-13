import uuid

# Databases services
from src.services.DataBaseService import DataBaseService

# Utils
from src.utils.format_datetime import format_datetime

conn = DataBaseService()


class ReviewsModel():

    def __init__(self, id=None, product_id=None, rating=None, user_id=None, username=None, review=None,
                 product_name=None, image_url=None, created_at=None, updated_at=None):
        """
        Represents a model for managing product reviews.

        Attributes:
            id (str): The unique identifier of the review.
            product_id (str): The unique identifier of the product.
            rating (int): The rating given to the product.
            user_id (str): The unique identifier of the user who wrote the review.
            username (str): The username of the user who wrote the review.
            review (str): The content of the review.
            product_name (str): The name of the product.
            image_url (str): The URL of the product image.
            created_at (datetime): The timestamp when the review was created.
            updated_at (datetime): The timestamp when the review was last updated.
        """
        self.id = id
        self.user_id = user_id
        self.username = username
        self.product_id = product_id
        self.rating = rating
        self.review = review
        self.product_name = product_name
        self.image_url = image_url
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def get_by_user(cls, user_id):
        """
        Retrieve reviews by user ID.
        """
        try:
            cursor = conn.get_cursor()
            sql = """
                SELECT
                    COALESCE(r.id, '') AS review_id,
                    i.product_id,
                    p.name,
                    COALESCE(img.image_url, '') AS image,
                    COALESCE(MAX(r.rating), 0) AS rating
                FROM
                    orders o
                INNER JOIN
                    order_items i ON o.id = i.order_id
                INNER JOIN
                    products p ON p.id = i.product_id
                LEFT JOIN
                    product_reviews r ON r.product_id = i.product_id AND r.user_id = o.customer_id
                LEFT JOIN
                    products_images img ON img.product_id = i.product_id AND img.is_main = TRUE
                WHERE
                    o.customer_id = %s
                GROUP BY 
                    i.product_id, r.id, p.name, img.image_url
                ORDER BY
                    MIN(i.added_at) DESC;
            """
            cursor.execute(sql, (user_id,))
            reviews = cursor.fetchall()
            if reviews is not None:
                return reviews
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def create(self):
        """
        Creates a new product review.

        Returns:
            str: The result of the review creation. Possible values are:
                - 'not_purchased': If the user has not purchased the product.
                - 'already_exists': If the user has already reviewed the product.
                - 'success': If the review was successfully created.
        """
        try:
            cursor = conn.get_cursor()
            sql = """
                SELECT 
                    i.product_id
                FROM
                    orders o
                        INNER JOIN
                    order_items i ON o.id = i.order_id
                WHERE
                    i.product_id = %s
                        AND o.customer_id = %s
                """
            cursor.execute(sql, (self.product_id, self.user_id,))
            result = cursor.fetchone()
            if result is None:
                return 'not_purchased'
            sql = """
                SELECT
                    r.product_id
                FROM
                    product_reviews r
                WHERE
                    r.product_id = %s
                        AND r.user_id = %s
                """
            cursor.execute(sql, (self.product_id, self.user_id,))
            result = cursor.fetchone()
            if result is not None:
                return 'already_exists'
            sql = """
                INSERT INTO product_reviews (
                    id,
                    product_id,
                    user_id,
                    rating,
                    review
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                );
                """
            cursor.execute(sql, (str(uuid.uuid4()), self.product_id,
                           self.user_id, self.rating, self.review,))
            conn.connection.commit()
            return 'success'
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get(cls, user_id, review_id):
        """
        Retrieves a review from the database based on the given user ID and review ID.
        """
        try:
            cursor = conn.get_cursor()
            sql = """
                SELECT 
                    r.id,
                    p.name,
                    COALESCE(img.image_url, '') AS image_url,
                    r.rating,
                    r.review
                FROM
                    product_reviews r
                INNER JOIN
                    products p ON p.id = r.product_id
                LEFT JOIN
                    products_images img ON img.product_id = p.id AND img.is_main = TRUE
                WHERE
                    r.id = %s AND r.user_id = %s;
                        """
            cursor.execute(sql, (review_id, user_id,))
            review = cursor.fetchone()
            if review is not None:
                return review
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def update(self):
        """
        Updates the rating and review of a product review.
        """
        try:
            cursor = conn.get_cursor()
            sql = """
                SELECT 
                    id
                FROM
                    product_reviews
                WHERE
                    id = %s AND user_id = %s;
                    """
            cursor.execute(sql, (self.id, self.user_id,))
            result = cursor.fetchone()
            if result is None:
                return 'not_exists'
            sql = """
                UPDATE product_reviews 
                SET 
                    rating = %s,
                    review = %s
                WHERE
                    id = %s AND user_id = %s;
                    """
            cursor.execute(
                sql, (self.rating, self.review, self.id, self.user_id,))
            conn.connection.commit()
            return 'success'
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get_by_product(cls, product_id):
        """
        Retrieve reviews for a specific product.
        """
        try:
            cursor = conn.get_cursor()
            sql = """
                SELECT
                    r.id,
                    r.rating,
                    r.review,
                    u.username,
                    r.created_at,
                    r.updated_at
                FROM
                    product_reviews r
                INNER JOIN
                    users u ON u.id = r.user_id
                WHERE
                    r.product_id = %s AND u.user_type != 'admin'
                ORDER BY
                    r.created_at DESC;
            """
            cursor.execute(sql, (product_id,))
            reviews = cursor.fetchall()
            if reviews is not None:
                return reviews
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def to_dict(self):
        """
        Converts the ReviewsModel object to a dictionary.
        """
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'product_id': self.product_id,
            'rating': self.rating,
            'review': self.review,
            'product_name': self.product_name,
            'image_url': self.image_url,
            'created_at': format_datetime(self.created_at),
            'updated_at': format_datetime(self.updated_at)
        }
        return {key: value for key, value in data.items() if value is not None}
