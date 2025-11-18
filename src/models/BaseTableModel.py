from abc import ABC, abstractmethod
from .DatabaseConnection import execute_query, FetchMode
from src.cache import cache

class BaseTableModel(ABC):

    def __init__(self, table_name : str, primary : str, columns : list[str]):
        self.table_name : str = table_name
        self.primary : str = primary
        self.columns : list[str] = columns

    def __repr__(self):
        return f"{self.__class__.__name__}{self.table_name}"

    def get_record(self, id: str) -> dict[str, int | str]:
        """
        Read one data from the table. The method returns a dictionary as the result.
        """

        return execute_query(
            query = f"SELECT * FROM {self.table_name} WHERE {self.primary} = %s",
            params = (id, ),
            fetch = FetchMode.ONE,
            as_dict = True
        )

    @cache.memoize(timeout=300)
    def get_all_records(self) -> list[dict]:
        """
        Gets all records from the table.
        """

        return execute_query(
            query = f"SELECT * FROM {self.table_name}",
            fetch = FetchMode.ALL,
            as_dict = True
        )

    @cache.memoize(timeout=300)
    def get_filtered_records(
            self,
            search_value : str,
            sort_column : str,
            sort_dir : str,
            limit : int,
            offset : int
        ) -> list[dict]:
        """
        Gets all filtered records from the table.
        """
        search_query = " OR ".join([f"text({col}) ILIKE %s" for col in self.columns])
        params = tuple( [f"%{search_value}%"] * len(self.columns) )

        return execute_query(
            query = (
                "SELECT * \n"
                f"FROM {self.table_name} \n"
                f"WHERE {search_query} "
                f"ORDER BY {sort_column} {sort_dir} "
                f"LIMIT {limit} OFFSET {offset}"
            ),
            params = params,
            fetch = FetchMode.ALL,
            as_dict = True
        )

    @cache.memoize(timeout=300)
    def get_total_filtered_records(
            self,
            search_value : str
        ) -> int:
        """
        Gets the total number of filtered records from the table.
        """
        search_query = " OR ".join([f"text({col}) ILIKE %s" for col in self.columns])
        params = tuple([f"%{search_value}%"] * len(self.columns))
        return execute_query(
            query = (
                "SELECT COUNT(*) "
                f"FROM {self.table_name} "
                f"WHERE {search_query}"
            ),
            params = params,
            fetch = FetchMode.ONE,
        )[0]

    @cache.memoize(timeout=300)
    def get_all_pkeys(self) -> list[dict]:
        """
        Gets all primary keys from the table.
        """
        return execute_query(
            query = (
                f"SELECT {self.primary} "
                f"FROM {self.table_name} "
                f"ORDER BY {self.primary} ASC"
            ),
            fetch = FetchMode.ALL,
            as_dict = True
        )

    def record_exists(
        self,
        column : str,
        value : str
    ) -> bool :
        """
        Check if a record already  exists in the table. Usually used for unique value checking.
        """

        return execute_query(
            query = f"SELECT 1 FROM {self.table_name} WHERE {column}=%s",
            params = (value,),
            fetch = FetchMode.ONE
        ) is not None

    def create(self, data : dict):
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
                f"INSERT INTO {self.table_name} ({col_query}) "
                f"VALUES ({param_plcholders})"
            ),
            params = params
        )

        self.general_cache_clear()

    def delete(self, key : str):
        """
        Deletes data from the table based on the primary key.
        """

        execute_query(
            query = f"DELETE FROM {self.table_name} WHERE {self.primary} = %s",
            params = (key,)
        )

        self.general_cache_clear()

    def update(self, orig_key : str, data : dict):
        """
        Update a record for the table.
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
                f"UPDATE {self.table_name} {set_query} "
                f"WHERE {self.primary} = %s"
            ),
            params = values
        )

        self.general_cache_clear()

    @cache.memoize(timeout=300)
    def get_total(self) -> int:
        """
        Gets the total number of rows from the table.
        """

        return execute_query(
            query = f"SELECT COUNT(*) FROM {self.table_name}",
            fetch = FetchMode.ONE,
        )[0]

    def general_cache_clear(self):
        cache.delete_memoized(self.get_all_records)
        cache.delete_memoized(self.get_filtered_records)
        cache.delete_memoized(self.get_total_filtered_records)
        cache.delete_memoized(self.get_total)