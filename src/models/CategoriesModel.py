import uuid

# Databases services
from src.services.DataBaseService import DataBaseService

conn = DataBaseService()


class CategoriesModel():

    def __init__(self, id, name, image_url):
        self.id = id if id is not None else str(uuid.uuid4())
        self. name = name
        self.image_url = image_url if image_url else ""

    @classmethod
    def get(cls):
        try:
            cursor = conn.get_cursor()
            cursor.callproc('Get_categories')
            for result in cursor.stored_results():
                categories = result.fetchall()
            if categories:
                return categories
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def create(self):
        try:
            cursor = conn.get_cursor()
            cursor.callproc('Create_category',
                            (self.id, self.name, self.image_url,))
            for result in cursor.stored_results():
                categories = result.fetchone()[0]
            if categories:
                conn.connection.commit()
                return categories
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def update(self):
        try:
            cursor = conn.get_cursor()
            cursor.callproc('Update_category',
                            (self.id, self.name, self.image_url,))
            for result in cursor.stored_results():
                categories = result.fetchone()[0]
            if categories:
                conn.connection.commit()
                return categories
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def to_dict(self):
        categories = {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
        }
        return categories
