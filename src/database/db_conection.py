from mysql.connector import connect
from src.utils.decorators.Singelton import singelton
import os


@singelton
class DBConnection():

    def __init__(self):
        try:
            self.connection = connect(
                host=os.getenv('MYSQL_HOST'),
                port=int(os.getenv('MYSQL_PORT')),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DB')
            )
        except Exception as ex:
            print("Error:", ex)
            self.connection = None
