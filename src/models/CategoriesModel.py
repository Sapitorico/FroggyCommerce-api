import uuid

# Databases services
from src.services.DataBaseService import DataBaseService

conn = DataBaseService()


class CategoriesModel():
    """
    Represents a category in the e-commerce system.

    Attributes:
        id (str): The unique identifier of the category.
        name (str): The name of the category.
        image_url (str): The URL of the category's image.
    """

    def __init__(self, id=None, name=None, image_url=None):
        self.id = id
        self.name = name
        self.image_url = image_url if image_url else ""

    @classmethod
    def get(cls):
        """
        Retrieves all categories from the database.
        """
        try:
            cursor = conn.get_cursor()

            sql = "SELECT id, name, image_url FROM categories;"
            cursor.execute(sql)
            categories = cursor.fetchall()

            if categories:
                return categories, 'success'
            return None, 'not_available'
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, 'failure'
        finally:
            conn.close()

    def create(self):
        """
        Creates a new category in the database.
        """
        try:
            cursor = conn.get_cursor()

            sql = "SELECT id FROM categories WHERE name = %s"
            cursor.execute(sql, (self.name,))
            result = cursor.fetchone()
            if result:
                return 'already_exists'

            sql = """
            INSERT INTO categories
                (id,
                name, 
                image_url)
            VALUES 
                (%s,
                %s,
                %s);
            """
            cursor.execute(
                sql, (str(uuid.uuid4()), self.name, self.image_url,))
            return 'success'
        except Exception as e:
            conn.connection.rollback()
            print(f"An error occurred: {e}")
            return 'failure'
        finally:
            conn.close()

    def update(self):
        """
        Updates an existing category in the database.
        """
        try:
            cursor = conn.get_cursor()

            sql = "SELECT id FROM categories WHERE id = %s"
            cursor.execute(sql, (self.id,))
            result = cursor.fetchone()

            if not result:
                return 'not_found'

            sql = "SELECT id FROM categories WHERE name = %s AND id != %s;"
            cursor.execute(sql, (self.name, self.id,))
            result = cursor.fetchone()

            if result:
                return 'already_exists'

            sql = """
            UPDATE
                categories
            SET
                name = %s,
                image_url = %s
            WHERE
                id = %s;
            """
            cursor.execute(sql, (self.name, self.image_url, self.id,))
            conn.connection.commit()
            return 'success'
        except Exception as e:
            conn.connection.rollback()
            print(f"An error occurred: {e}")
            return 'failure'
        finally:
            conn.close()

    def to_dict(self):
        """
        Converts the category object to a dictionary.
        """
        categories = {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
        }
        return categories
