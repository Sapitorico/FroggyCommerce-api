import unittest
from mysql.connector import connect, ProgrammingError
import subprocess
from flask import Flask
import os

from dotenv import load_dotenv

load_dotenv()


current_directory = os.path.dirname(os.path.abspath(__file__))



class BaseTestContext(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        script_path = os.path.join(current_directory, "create_db_test.sh")
        try:
            subprocess.run([script_path], check=True)
        except subprocess.CalledProcessError as e:
            print("Error al ejecutar el script create_db_test.sh:", e)
            exit(1)

        self.connection = connect(
            host=os.getenv('MYSQL_HOST_TEST'),
            port=int(os.getenv('MYSQL_PORT_TEST')),
            user=os.getenv('MYSQL_USER_TEST'),
            password=os.getenv('MYSQL_PASSWORD_TEST'),
            database=os.getenv('MYSQL_DB_TEST')
        )

    def tearDown(self):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                f"DROP DATABASE IF EXISTS {os.getenv('MYSQL_DB_TEST')}")
            self.connection.commit()
            self.cursor.close()
        except ProgrammingError as err:
            print("Error al ejecutar el script SQL:", err)
            exit(1)
        self.connection.close()
        self.app_context.pop()
