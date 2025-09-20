from abc import ABC, abstractmethod
from .DatabaseConnection import DatabaseConnection

class BaseTableModel(ABC):

    _table_name : str = None
    _primary : str = None
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
            sql = f"SELECT * FROM {cls.get_table_name()}"
            cursor.execute(sql)

            result = cursor.fetchall()
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
    def delete(cls, key : str):
        """
        Deletes data from the table based on the primary key.
        """
        cls.initialize()

        try:
            cursor = DatabaseConnection.get_connection().cursor()
            sql = f"DELETE FROM {cls._tableName} WHERE {cls._primary} = {key})"
            cursor.execute(sql)
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