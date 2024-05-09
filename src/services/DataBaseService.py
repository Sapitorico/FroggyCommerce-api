import logging
from src.decorators.Singelton import singelton
from mysql.connector import connect
import os


@singelton
class DataBaseService():
    """
    A class that provides database connection and cursor functionality.
    """

    def __init__(self):
        """
        Initializes a new instance of the DataBasesService class.
        """
        self.connection = self.connection()
        self.cursor = self.get_cursor()

    def connection(self):
        """
        Establishes a connection to the database.

        Returns:
            The database connection object.
        """
        try:
            return connect(
                host=os.getenv('MYSQL_HOST'),
                port=int(os.getenv('MYSQL_PORT')),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DB')
            )
        except Exception as e:
            logging.error(f"MySQL Error: {str(e)}")
            return None

    def get_cursor(self):
        """
        Retrieves the cursor object associated with the database connection.

        Returns:
            The cursor object.
        """
        if self.connection:
            return self.connection.cursor()
        else:
            return None

    def close(self):
        """
        Closes the cursor.
        """
        if self.cursor:
            self.cursor.close()

