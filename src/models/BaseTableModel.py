from abc import ABC, abstractmethod
from .DatabaseConnection import DatabaseConnection

class BaseTableModel(ABC):

    _table_name : str = None
    _primary : str = None
    _columns : list[str] = None
    _initialized : bool = False

    @classmethod
    def initialize(cls):
        """
        Initializes the table by creating it if it does not exist."
        """
        try:
            cursor = DatabaseConnection.get_connection().cursor()
            if not cls._initialized:
                cls._initialized = True
                cls._create_table()
                cursor.execute("""
                    SELECT attname
                    FROM pg_attribute
                    WHERE attrelid = %s::regclass
                    AND attnum > 0
                    AND NOT attisdropped;
                """, (cls.get_table_name(),))
                cls._columns = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
    
    @classmethod  
    @abstractmethod
    def _create_table(cls):
        """
        Creates the table in the database. This method should be implemented by
        subclasses to create the specific table. The method should also handle
        any exceptions that may occur during the table creation process.
        Should only be called once when the table is initialized.
        """
        pass

    @classmethod
    def get_table_name(cls) -> str:
        """
        Returns the name of the table.
        """
        cls.initialize()
        return cls._table_name

    @classmethod
    def get_primary_key(cls) -> str:
        """
        Returns the primary key of the table.
        """
        cls.initialize()
        return cls._primary

    @classmethod
    def get_columns(cls) -> list[str]:
        """
        Returns the columns of the table.
        """
        return cls._columns

    @classmethod
    def get_record(cls, id: str) -> dict[str, int | str]:
        """
        Read one data from the table. The method returns a dictionary as the result.
        """
        cls.initialize()

        result = {}

        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            sql = f"SELECT * FROM {cls.get_table_name()} WHERE {cls.get_primary_key()} = {id}"
            cursor.execute(sql)

            result = cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

        return result

    @classmethod
    def get_aLL_records(cls) -> list[dict]:
        """
        Gets all records from the table.
        """
        cls.initialize()

        result = []

        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            query = f"SELECT * FROM {cls.get_table_name()}"
            cursor.execute(query)

            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

        return result
    
    @classmethod
    def get_filtered_records(
            cls,
            search_value : str,
            sort_column : str,
            sort_dir : str,
            limit : int,
            offset : int
        ) -> list[dict]:
        """
        Gets all filtered records from the table.
        """
        cls.initialize()

        result = []

        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            search_clause = " OR ".join([f"text(\"{col}\") ILIKE %s" for col in cls.get_columns()])
            query = f"""
                SELECT * 
                FROM {cls.get_table_name()} 
                WHERE {search_clause}
                ORDER BY \"{sort_column}\" {sort_dir}
                LIMIT {limit} OFFSET {offset};
            """
            params = tuple([f"%{search_value}%"] * len(cls.get_columns()))
            cursor.execute(query, params)

            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

        return result

    @classmethod
    def get_total_filtered_records(
            cls,
            search_value : str
        ) -> int:
        """
        Gets the total number of filtered records from the table.
        """
        cls.initialize()

        result = []

        try:
            cursor = DatabaseConnection.get_connection().cursor()
            search_clause = " OR ".join([f"text(\"{col}\") ILIKE %s" for col in cls.get_columns()])
            query = f"""
                SELECT COUNT(*) 
                FROM {cls.get_table_name()} 
                WHERE {search_clause}
            """
            params = tuple([f"%{search_value}%"] * len(cls.get_columns()))
            cursor.execute(query, params)

            result = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

        return result

    @classmethod
    def get_aLL_pkeys(cls) -> list[dict]:
        """
        Gets all primary keys from the table.
        """
        cls.initialize()

        result = []

        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            sql = f"SELECT \"{cls.get_primary_key()}\" FROM {cls.get_table_name()}"
            cursor.execute(sql)

            result = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

        return result

    @classmethod
    def record_exists(
        cls,
        column : str,
        value : str
    ) -> bool :
        """
        Check if a record already  exists in the table. Usually used for unique value checking.
        """

        cls.initialize()

        result = False
        try:
            cursor = DatabaseConnection.get_connection().cursor()

            query = f"SELECT 1 FROM {cls.get_table_name()} WHERE \"{column}\"=%s"
            cursor.execute(query, (value,))
            result = True if cursor.fetchone() else False
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result

    @classmethod
    def create(cls, data : dict):
        """
        Creates a new record for the table.
        """

        cls.initialize()

        try:
            cursor = DatabaseConnection.get_connection().cursor()
            columns = []
            values = []
            for key,value in data.items():
                columns.append(key)
                values.append(value)

            columns_str = ",".join([f"\"{col}\"" for col in columns])
            values_str = ",".join([f"%s" for value in values])
            values = tuple(values)
            query = f"INSERT INTO {cls.get_table_name()} ({columns_str}) VALUES ({values_str})"
            cursor.execute(query, values)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def delete(cls, key : str):
        """
        Deletes data from the table based on the primary key.
        """
        cls.initialize()

        try:
            cursor = DatabaseConnection.get_connection().cursor()
            sql = f"DELETE FROM {cls.get_table_name()} WHERE \"{cls._primary}\" = %s"
            cursor.execute(sql, (key,))
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def get_total(cls) -> int:
        """
        Gets the total number of rows from the table.
        """
        cls.initialize()

        total = 0
        try:
            cursor = DatabaseConnection.get_connection().cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {cls.get_table_name()};")
            total = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return total