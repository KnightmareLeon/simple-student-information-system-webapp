from flask_login import UserMixin
from werkzeug.security import check_password_hash

from .DatabaseConnection import execute_query, FetchMode

class User(UserMixin):

    def __init__(
        self,
        id : int = None,
        username : str = None,
        password : str = None
    ):

        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def get_by_id(cls, user_id):
        res = execute_query(
            query = f"SELECT * FROM users WHERE id = %s",
            params = (user_id,),
            fetch = FetchMode.ONE,
            as_dict = True
        )
        return cls(
            res["id"],
            username = res["username"],
            password = res["password"]
        ) if res else None

    @classmethod
    def get_by_username(cls, user_username):
        res = execute_query(
            query = f"SELECT * FROM users WHERE username = %s",
            params = (user_username,),
            fetch = FetchMode.ONE,
            as_dict = True
        )
        return cls(
            res["id"],
            username = res["username"],
            password = res["password"]
        ) if res else None

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)