import uuid

# Security
from src.services.DataBaseService import DataBaseService

# Database connection
from src.services.SecurityService import SecurityService

# Utils
from src.utils.format_datetime import format_datetime

# Database connection:
conn = DataBaseService()


class UsersModel():
    """
    Represents a user in the e-commerce system.

    Attributes:
        id (str): The unique identifier of the user.
        full_name (str): The full name of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        phone_number (str): The phone number of the user.
        password (str): The password of the user. Defaults to None.
        user_type (str): The type of the user. Defaults to None.
        created_at (datetime): The timestamp when the user was created. Defaults to None.
        updated_at (datetime): The timestamp when the user was last updated. Defaults to None.
    """

    def __init__(self, id=None, full_name=None, username=None, email=None, phone_number=None,
                 password=None, user_type=None, created_at=None, updated_at=None):
        self.id = id
        self.full_name = full_name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.user_type = user_type
        self.created_at = created_at
        self.updated_at = updated_at

    def create(self):
        """
        Creates a new user in the database.
        """
        try:
            cursor = conn.get_cursor()

            sql = """
            SELECT 
                id
            FROM
                users
            WHERE
                email = %s
                    OR full_name = %s
                    OR username = %s
                    OR phone_number = %s;
            """
            cursor.execute(sql, (self.email, self.full_name,
                           self.username, self.phone_number,))
            result = cursor.fetchone()

            if result:
                return None, 'already_exists'

            sql = """
                INSERT INTO users (
                    id,
                    full_name,
                    username,
                    email,
                    phone_number,
                    password
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                );
            """
            cursor.execute(sql, (str(uuid.uuid4()), self.full_name, self.username, self.email,
                                 self.phone_number, SecurityService.hash_password(self.password),))

            conn.connection.commit()

            return self.full_name, 'success'
        except Exception as e:
            conn.connection.rollback()
            print(f"An error occurred: {e}")
            return None, 'failure'
        finally:
            conn.close()

    @classmethod
    def get(cls, email):
        """
        Retrieves a user from the database based on the provided data.
        """
        try:
            cursor = conn.get_cursor()

            sql = """
            SELECT 
                id,
                full_name,
                username,
                email,
                phone_number,
                password,
                user_type,
                created_at,
                updated_at
            FROM
                users
            WHERE
                email = %s;
            """
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

            if user:
                return user, 'success'
            return None, 'not_found'
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, 'failure'
        finally:
            conn.close()

    @classmethod
    def get_all(cls, page, per_page, name=None):
        """
        Retrieves all users from the database.
        """
        try:
            cursor = conn.get_cursor()

            sql = """
            SELECT
                CEIL(COUNT(*) / %s)
            FROM
                users u
            WHERE
                u.user_type = 'customer'
                AND (%s IS NULL OR u.full_name LIKE CONCAT(%s, '%%'))
            """

            cursor.execute(sql, (per_page, name, name))
            total_pages = cursor.fetchone()[0]

            offset = (page - 1) * per_page

            sql = """
                SELECT 
                    id,
                    full_name,
                    username,
                    email,
                    phone_number,
                    user_type,
                    created_at,
                    updated_at
                FROM
                    users u
                WHERE
                    user_type = 'customer'
                    AND (%s IS NULL OR u.full_name LIKE CONCAT(%s, '%%'))
                ORDER BY u.created_at DESC
                LIMIT %s
                OFFSET %s;
            """

            cursor.execute(sql, (name, name, per_page, offset,))
            users = cursor.fetchall()

            if users:
                return users, total_pages, 'success'
            return None, None, 'not_found'
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None, 'failure'
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, id):
        """
        Retrieves a user from the database based on the provided ID.
        """
        try:
            cursor = conn.get_cursor()
            
            sql = """
                SELECT 
                    id,
                    full_name,
                    username,
                    email,
                    phone_number,
                    user_type,
                    created_at,
                    updated_at
                FROM
                    users
                WHERE
                    id = %s;
            """
            cursor.execute(sql, (id,))
            user = cursor.fetchone()
            
            if user:
                return user, 'success'
            return None, 'not_found'
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, 'failure'
        finally:
            conn.close()

    def update(self):
        """
        Updates the user in the database.
        """
        try:
            cursor = conn.get_cursor()
            
            sql = """
            SELECT 
                id
            FROM
                users
            WHERE
                id = %s
            """
            cursor.execute(sql, (self.id,))
            result = cursor.fetchone()
            
            if not result:
                return 'not_exists'
            sql = """
            SELECT 
                id
            FROM
                users
            WHERE
                (email = %s
                OR full_name = %s
                OR username = %s
                OR phone_number = %s)
                AND id != %s
            """
            cursor.execute(sql, (self.email, self.full_name,
                           self.username, self.phone_number, self.id))
            result = cursor.fetchone()
            if result:
                return 'already_exists'
            sql = """
            UPDATE users 
            SET 
                full_name = %s,
                username = %s,
                email = %s,
                phone_number = %s
            WHERE
                id = %s;
            """
            cursor.execute(sql, (self.full_name, self.username,
                           self.email, self.phone_number, self.id,))
            conn.connection.commit()
            return 'success'
        except Exception as e:
            conn.connection.rollback()
            print(f"An error occurred: {e}")
            return'failure'
        finally:
            conn.close()

    @classmethod
    def delete(cls, id):
        """
        Deletes a user from the database based on the provided ID.
        """
        try:
            cursor = conn.get_cursor()
            
            sql = """
            SELECT 
                id
            FROM
                users
            WHERE
                id = %s AND user_type != 'admin';
            """
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            
            if not result:
                return 'not_exists'
            
            sql = "DELETE FROM cart WHERE customer_id = %s;"
            cursor.execute(sql, (id,))
            
            sql = "DELETE FROM users WHERE id = %s AND user_type != 'admin';"
            cursor.execute(sql, (id,))
            
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
        Converts the user object to a dictionary.
        """
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "user_type": self.user_type,
            "created_at": format_datetime(self.created_at),
            "updated_at": format_datetime(self.updated_at)
        }
        return {key: value for key, value in data.items() if value is not None}
