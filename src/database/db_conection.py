from mysql.connector import connect
from src.utils.decorators.Singelton import singelton
import os


@singelton
class DBConnection():
    """
    Class to handle database connections.
    """

    def __init__(self):
        """
        Initialize DBConnection class.

        Attempts to establish a connection with the MySQL database using environment variables.
        """

        try:
            self.connection = connect(
                host=os.getenv('MYSQL_HOST'),
                port=int(os.getenv('MYSQL_PORT')),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DB')
            )
        except Exception as e:
            self.connection = None
            print(f"Error: {str(e)}")
