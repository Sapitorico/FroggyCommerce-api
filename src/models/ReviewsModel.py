import uuid

# Databases services
from src.services.DataBaseService import DataBaseService

conn = DataBaseService()


class ReviewsModel():

    def __init__(self, id=None, product_id=None, rating=None, user_id=None, username=None, review=None,
                 product_name=None, image_url=None, created_at=None, updated_at=None):
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
        try:
            cursor = conn.get_cursor()
            cursor.callproc('User_reviews', (user_id,))
            for result in cursor.stored_results():
                reviews = result.fetchall()
            if reviews:
                return reviews
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def create(self):
        try:
            cursor = conn.get_cursor()
            cursor.callproc('Create_review', (self.user_id,
                            self.product_id, str(uuid.uuid4()), self.rating, self.review))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message:
                conn.connection.commit()
                return message
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get(cls, user_id, review_id):
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
            if review:
                return review
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def update(self):
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
            if not result:
                return None
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
            return True
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get_by_product(cls, product_id):
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
            result = cursor.fetchall()
            print(result)
            if result:
                return result
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'product_id': self.product_id,
            'rating': self.rating,
            'review': self.review,
            'product_name': self.product_name,
            'image_url': self.image_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
        return {key: value for key, value in data.items() if value is not None}
