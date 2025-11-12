from psycopg2 import pool
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2 import errors

from config import HOST, USER, PASSWORD, PORT, DATABASE

from enum import Enum

class FetchMode(Enum):
    NONE = 'none'
    ONE = 'one'
    ALL = 'all'

_connection_pool : pool.SimpleConnectionPool = None

def start_pool():
    global _connection_pool
    if _connection_pool is not None:
        return

    _connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=HOST,
        user=USER,
        password=PASSWORD,
        dbname=DATABASE,
        port=PORT,
        sslmode="require"
    )

def get_connection():
    global _connection_pool
    if _connection_pool is None:
        start_pool()
    return _connection_pool.getconn()

def release_connection(conn):
    global _connection_pool
    if _connection_pool:
        _connection_pool.putconn(conn)

def close_pool():
    global _connection_pool
    if _connection_pool:
        _connection_pool.closeall()
        _connection_pool = None

def execute_query(
        query : str,
        params : tuple | None = None,
        fetch : FetchMode = FetchMode.NONE,
        as_dict : bool = False
    ) -> list[tuple] | list[RealDictRow] | None:
    """
    Helper function for executing database queries. \n
    The parameters are as follows:
    - query (required) : str - the query that will be executed
    - params (default: None): tuple | None  - the parameters that will be formatted into the query
    - fetch (default: FetchMode.NONE): FetchMode - how the results will be fetched
    - as_dict (default: False): bool - returns fetch results as a list of dictionaries instead of tuples
    
    The function will either return a list of tuples or dictionaries, or none, depending on the
    provided arguments.
    """
    try:
        db = get_connection()
        if as_dict:
            cursor = db.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = db.cursor()

        cursor.execute(query, params or ())

        result = None
        if fetch == FetchMode.ONE:
            result = cursor.fetchone()
        elif fetch == FetchMode.ALL:
            result = cursor.fetchall()
        db.commit()
        return result

    except errors.UniqueViolation as e:
        print(f"Error: {e}")
        db.rollback()
        raise e
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise e

    finally:
        cursor.close()
        release_connection(db)