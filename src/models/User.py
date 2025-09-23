from flask_login import UserMixin
from werkzeug.security import check_password_hash

from .DatabaseConnection import DatabaseConnection

class User(UserMixin):

    def __init__(
        self,
        id = None,
        username = None,
        password = None
    ):

        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def get_by_id(cls, user_id):
        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            query = f"SELECT * FROM users WHERE \"ID\" = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return cls(result["ID"], username=result["Username"], password=result["Password"])
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return None

    @classmethod
    def get_by_username(cls, user_username):
        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            query = f"SELECT * FROM users WHERE \"Username\" = %s"
            cursor.execute(query, (user_username,))
            result = cursor.fetchone()
            if result:
                return cls(result["ID"], username=result["Username"], password=result["Password"])
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return None

    def check_password(self, password) -> bool:
        print(self.password)
        print(password)
        return check_password_hash(self.password, password)