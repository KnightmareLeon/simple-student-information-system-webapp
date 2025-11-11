from abc import ABC, abstractmethod
from .DatabaseConnection import execute_query, FetchMode

class BaseTableModel(ABC):

    _table_name : str = None
    _primary : str = None
    _columns : list[str] = None

    @classmethod
    def get_table_name(cls) -> str:
        """
        Returns the name of the table.
        """
        return cls._table_name

    @classmethod
    def get_primary_key(cls) -> str:
        """
        Returns the primary key of the table.
        """
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

        return execute_query(
            query = f"SELECT * FROM {cls.get_table_name()} WHERE {cls.get_primary_key()} = %s",
            params = (id, ),
            fetch = FetchMode.ONE,
            as_dict = True
        )

    @classmethod
    def get_aLL_records(cls) -> list[dict]:
        """
        Gets all records from the table.
        """

        return execute_query(
            query = f"SELECT * FROM {cls.get_table_name()}",
            fetch = FetchMode.ALL,
            as_dict = True
        )
    
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
        search_query = " OR ".join([f"text({col}) ILIKE %s" for col in cls.get_columns()])
        params = tuple( [f"%{search_value}%"] * len(cls.get_columns()) )

        return execute_query(
            query = (
                "SELECT * \n"
                f"FROM {cls.get_table_name()} \n"
                f"WHERE {search_query} "
                f"ORDER BY {sort_column} {sort_dir} "
                f"LIMIT {limit} OFFSET {offset}"
            ),
            params = params,
            fetch = FetchMode.ALL,
            as_dict = True
        )

    @classmethod
    def get_total_filtered_records(
            cls,
            search_value : str
        ) -> int:
        """
        Gets the total number of filtered records from the table.
        """
        search_query = " OR ".join([f"text({col}) ILIKE %s" for col in cls.get_columns()])
        params = tuple([f"%{search_value}%"] * len(cls.get_columns()))
        return execute_query(
            query = (
                "SELECT COUNT(*) "
                f"FROM {cls.get_table_name()} "
                f"WHERE {search_query}"
            ),
            params = params,
            fetch = FetchMode.ONE,
        )[0]

    @classmethod
    def get_all_pkeys(cls) -> list[dict]:
        """
        Gets all primary keys from the table.
        """
        return execute_query(
            query = (
                f"SELECT {cls.get_primary_key()} "
                f"FROM {cls.get_table_name()} "
                f"ORDER BY {cls.get_primary_key()} ASC"
            ),
            fetch = FetchMode.ALL,
            as_dict = True
        )

    @classmethod
    def record_exists(
        cls,
        column : str,
        value : str
    ) -> bool :
        """
        Check if a record already  exists in the table. Usually used for unique value checking.
        """

        return execute_query(
            query = f"SELECT 1 FROM {cls.get_table_name()} WHERE {column}=%s",
            params = (value,),
            fetch = FetchMode.ONE
        ) is not None

    @classmethod
    def create(cls, data : dict):
        """
        Creates a new record for the table.
        """

        columns = []
        values = []
        for key,value in data.items():
            columns.append(key)
            values.append(value)

        col_query = ",".join([f"{col}" for col in columns])
        param_plcholders = ",".join([f"%s" for val in values])
        params = tuple(values)

        execute_query(
            query = (
                f"INSERT INTO {cls.get_table_name()} ({col_query}) "
                f"VALUES ({param_plcholders})"
            ),
            params = params
        )

    @classmethod
    def delete(cls, key : str):
        """
        Deletes data from the table based on the primary key.
        """

        execute_query(
            query = f"DELETE FROM {cls.get_table_name()} WHERE {cls._primary} = %s",
            params = (key,)
        )

    @classmethod
    def update(cls, orig_key : str, data : dict):
        """
        Creates a new record for the table.
        """
        columns = []
        values = []
        for key, value in data.items():
            columns.append(key)
            values.append(value)
        set_query = "SET " + " , ".join([f"{col} = %s "for col in columns])
        values.append(orig_key)
        values = tuple(values)

        execute_query(
            query = (
                f"UPDATE {cls.get_table_name()} {set_query} "
                f"WHERE {cls.get_primary_key()} = %s"
            ),
            params = values
        )

    @classmethod
    def get_total(cls) -> int:
        """
        Gets the total number of rows from the table.
        """

        return execute_query(
            query = f"SELECT COUNT(*) FROM {cls.get_table_name()}",
            fetch = FetchMode.ONE,
        )[0]