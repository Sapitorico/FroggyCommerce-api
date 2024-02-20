from mysql.connector import connect
import os

def connect_to_mysql():
    try:
        connection = connect(
            host=os.getenv('MYSQL_HOST'),
            port=int(os.getenv('MYSQL_PORT')),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )
        
        if connection.is_connected():
            print("Connected to MySQL database")
            info_server = connection.get_server_info()
            print("MySQL Server version:", info_server)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()[0]
            print("You're connected to database:", database_name)
            cursor.close()
            return connection
    except Exception as ex:
        print("Error:", ex)
        return None

