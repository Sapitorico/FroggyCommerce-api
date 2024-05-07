from mysql.connector import connect
from src.utils.decorators.Singelton import singelton
import os


@singelton
class DBConnection():
    """
    A class representing a database connection.

    This class provides methods to establish a connection to a MySQL database.

    Attributes:
        connection: The connection object to the MySQL database.

    Methods:
        __init__: Initializes the DBConnection object and establishes a connection to the database.
    """

    def __init__(self):
        """
        Initializes the DBConnection object and establishes a connection to the database.

        Raises:
            Exception: If an error occurs while establishing the connection.
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
