from src.models.DatabaseConnection import execute_query, FetchMode
from .BaseTableModel import BaseTableModel
from .StudentsModel import std_table as child_table, StudentsModel

from src.cache import cache

class ProgramsModel(BaseTableModel):
    """
    CREATE TABLE IF NOT EXISTS public.programs
    (
        code character varying(20) COLLATE pg_catalog."default" NOT NULL,
        name character varying(100) COLLATE pg_catalog."default" NOT NULL,
        collegecode character varying(5) COLLATE pg_catalog."default",
        CONSTRAINT programs_pkey PRIMARY KEY (code),
        CONSTRAINT unique_program_name UNIQUE (name),
        CONSTRAINT programs_fkey FOREIGN KEY (collegecode)
            REFERENCES public.colleges (code) MATCH SIMPLE
            ON UPDATE CASCADE
            ON DELETE SET NULL,
        CONSTRAINT program_code_format CHECK (code::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(code::text) <= 20),
        CONSTRAINT program_name_format CHECK (name::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(name::text) <= 100)
    )
    """

    def __init__(self, table_name: str, primary: str, columns: list[str], std_table: StudentsModel):
        super().__init__(table_name, primary, columns)
        self.std_table: StudentsModel = std_table

    def delete(self, key):
        self.general_cache_clear()
        cache.delete_memoized(self.program_info, key)
        self.std_table.general_cache_clear()
        cache.delete_memoized(self.std_table.students_info)
        super().delete(key)

    def update(self, orig_key, data):
        self.general_cache_clear()
        cache.delete_memoized(self.program_info, orig_key)
        self.std_table.general_cache_clear()
        cache.delete_memoized(self.std_table.students_info)
        super().update(orig_key, data)

    @cache.memoize(timeout=300)
    def total_programs_by_college(
        self,
        college_code : str
    ) -> int :
        """
        Returns the total number of programs under a college.
        """

        res = execute_query(
            query = (
                f"SELECT collegecode, COUNT(collegeCodec) "
                f"FROM {self.table_name} "
                f"WHERE collegecode = %s GROUP BY collegecode"
            ),
            params = (college_code,),
            fetch = FetchMode.ONE
        )
        return 0 if not res else res[1]
    
    @cache.memoize(timeout=300)
    def program_info(
        self,
        code : str
    ) -> dict[int | str] :
        """
        Returns the complete details of a program record along with
        the total students under it and  the college name that the program
        is under.
        """
        return execute_query(
            query = (
                "SELECT "
                "p.code, p.name, p.collegecode, "
                "c.name AS collegename, "
                "COUNT(s.programcode) AS totalstds "
                f"FROM {self.table_name} as p "
                "LEFT JOIN colleges as c ON p.collegecode = c.code "
                "LEFT JOIN students as s ON p.code = s.programcode "
                "WHERE p.code = %s "
                "GROUP BY p.code, p.name, p.collegecode, c.name" 
            ),
            params = (code,),
            fetch = FetchMode.ONE,
            as_dict = True
        )

prg_table : ProgramsModel = ProgramsModel(
    table_name="programs",
    primary="code",
    columns=["code","name","collegecode"],
    std_table=child_table
)