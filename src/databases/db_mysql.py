import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        return pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            port=int(os.getenv('MYSQL_PORT')),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            db=os.getenv('MYSQL_NAME')
        )
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    get_connection()