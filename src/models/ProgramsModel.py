from src.models.DatabaseConnection import execute_query, FetchMode
from .BaseTableModel import BaseTableModel

class ProgramsModel(BaseTableModel):

    _table_name = "programs"
    _primary = "code"
    _columns : list[str] = ["code", "name","collegecode"]

    # CREATE TABLE IF NOT EXISTS public.programs
    # (
    #     code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    #     name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #     collegecode character varying(5) COLLATE pg_catalog."default",
    #     CONSTRAINT programs_pkey PRIMARY KEY (code),
    #     CONSTRAINT unique_program_name UNIQUE (name),
    #     CONSTRAINT programs_fkey FOREIGN KEY (collegecode)
    #         REFERENCES public.colleges (code) MATCH SIMPLE
    #         ON UPDATE CASCADE
    #         ON DELETE SET NULL,
    #     CONSTRAINT program_code_format CHECK (code::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(code::text) <= 20),
    #     CONSTRAINT program_name_format CHECK (name::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(name::text) <= 100)
    # )

    @classmethod
    def total_programs_by_college(
        cls,
        college_code : str
    ) -> int :
        """
        Returns the total number of programs under a college.
        """

        res = execute_query(
            query = (
                f"SELECT collegecode, COUNT(collegeCodec) "
                f"FROM {cls.get_table_name()} "
                f"WHERE collegecode = %s GROUP BY collegecode"
            ),
            params = (college_code,),
            fetch = FetchMode.ONE
        )
        return 0 if not res else res[1]
    
    @classmethod
    def program_info(
        cls,
        code : str
    ) -> dict[int | str] :
        """
        Returns the complete details of a program record along with
        the total students under it and  the college name that the program
        is under.
        """
        result = None
        return execute_query(
            query = (
                "SELECT "
                "p.code, p.name, p.collegecode, "
                "c.name AS collegename, "
                "COUNT(s.programcode) AS totalstds "
                "FROM programs as p "
                "LEFT JOIN colleges as c ON p.collegecode = c.code "
                "LEFT JOIN students as s ON p.code = s.programcode "
                "WHERE p.code = %s "
                "GROUP BY p.code, p.name, p.collegecode, c.name" 
            ),
            params = (code,),
            fetch = FetchMode.ONE,
            as_dict = True
        )