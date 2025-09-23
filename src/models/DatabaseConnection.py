import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

class DatabaseConnection:
    """
    A singleton class to manage the database connection.
    """
    
    __db = None
    real_dict = psycopg2.extras.RealDictCursor

    @staticmethod
    def start_connection():
        """
        Initializes the database connection using the credentials stored in the .env file.
        """
        if DatabaseConnection.__db is not None:
            return
        
        load_dotenv()
        DatabaseConnection.__db = psycopg2.connect(
            host = os.getenv("HOST"),
            user = os.getenv("USER"),
            password = os.getenv("PASSWORD"),
            database = os.getenv("DATABASE")
        )
        DatabaseConnection.__db.autocommit = True

    @staticmethod
    def get_connection() -> psycopg2.extensions.connection:
        """
        Returns the database connection object. If the connection is not established,
        it initializes the connection first.
        """
        if DatabaseConnection.__db is None:
            DatabaseConnection.start_connection()
        return DatabaseConnection.__db

    @staticmethod
    def close_connection():
        """
        Closes the database connection if it is open.
        """
        if DatabaseConnection.__db is None:
            return
        if DatabaseConnection.__db.is_connected():
            DatabaseConnection.__db.close()