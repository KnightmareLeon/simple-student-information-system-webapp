from .DatabaseConnection import execute_query, FetchMode
from .BaseTableModel import BaseTableModel as Base

from src.cache import cache
from typing import Optional

class StudentsModel(Base):
    """
    CREATE TABLE IF NOT EXISTS public.students
    (
        id character(9) COLLATE pg_catalog."default" NOT NULL,
        firstname character varying(100) COLLATE pg_catalog."default" NOT NULL,
        lastname character varying(100) COLLATE pg_catalog."default" NOT NULL,
        gender gender NOT NULL,
        yearlevel year_level NOT NULL,
        programcode character varying(20) COLLATE pg_catalog."default",
        image text COLLATE pg_catalog."default",
        CONSTRAINT students_pkey PRIMARY KEY (id),
        CONSTRAINT students_fkey FOREIGN KEY (programcode)
            REFERENCES public.programs (code) MATCH SIMPLE
            ON UPDATE CASCADE
            ON DELETE SET NULL,
        CONSTRAINT first_name_format CHECK (firstname::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(firstname::text) <= 100),
        CONSTRAINT id_format CHECK (id ~ '^(?:19(?:6[7-9]|[7-9][0-9])|20[0-9]{2}|2100)-(?:000[1-9]|00[1-9][0-9]|0[1-9][0-9]{2}|[1-9][0-9]{3})$'::text),
        CONSTRAINT last_name_format CHECK (lastname::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(lastname::text) <= 100)
    )
    """
    @cache.memoize(timeout=300)
    def get_filtered_records(
            self,
            search_value: str,
            sort_column: str,
            sort_dir: str,
            limit: int,
            offset: int,
            gender: Optional[str] = None,
            yearlevel: Optional[str] = None,
            program_code: Optional[str] = None
        ) -> list[dict]:
        """
        Gets all filtered records from the table, optionally filtered by gender, yearlevel, and program_code.
        """
        search_query = " OR ".join([f"text({col}) ILIKE %s" for col in self.columns])
        params = [f"%{search_value}%"] * len(self.columns)

        filter_conditions = []

        # Only add filters if the value is meaningful
        if gender and str(gender).strip().lower() != "all" and str(gender).strip().lower() != "none":
            filter_conditions.append("gender = %s")
            params.append(gender)
        if yearlevel and str(yearlevel).strip().lower() != "all" and str(yearlevel).strip().lower() != "none":
            filter_conditions.append("yearlevel = %s")
            params.append(yearlevel)
        if program_code and str(program_code).strip().lower() != "all" and str(program_code).strip().lower() != "none":
            filter_conditions.append("programcode = %s")
            params.append(program_code)

        where_clause = f"({search_query})"
        if filter_conditions:
            where_clause += " AND " + " AND ".join(filter_conditions)

        query = (
            f"SELECT * \n"
            f"FROM {self.table_name} \n"
            f"WHERE {where_clause} "
            f"ORDER BY {sort_column} {sort_dir} "
            f"LIMIT {limit} OFFSET {offset}"
        )

        return execute_query(
            query=query,
            params=tuple(params),
            fetch=FetchMode.ALL,
            as_dict=True
        )


    @cache.memoize(timeout=300)
    def get_total_filtered_records(
            self,
            search_value: str,
            gender: Optional[str] = None,
            yearlevel: Optional[str] = None,
            program_code: Optional[str] = None
        ) -> int:
        """
        Gets the total number of filtered records from the table, optionally filtered by gender, yearlevel, and program_code.
        """
        search_query = " OR ".join([f"text({col}) ILIKE %s" for col in self.columns])
        params = [f"%{search_value}%"] * len(self.columns)

        filter_conditions = []

        if gender and str(gender).strip().lower() != "all" and str(gender).strip().lower() != "none":
            filter_conditions.append("gender = %s")
            params.append(gender)
        if yearlevel and str(yearlevel).strip().lower() != "all" and str(yearlevel).strip().lower() != "none":
            filter_conditions.append("yearlevel = %s")
            params.append(yearlevel)
        if program_code and str(program_code).strip().lower() != "all" and str(program_code).strip().lower() != "none":
            filter_conditions.append("programcode = %s")
            params.append(program_code)

        where_clause = f"({search_query})"
        if filter_conditions:
            where_clause += " AND " + " AND ".join(filter_conditions)

        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE {where_clause}"

        return execute_query(
            query=query,
            params=tuple(params),
            fetch=FetchMode.ONE
        )[0]

    @cache.memoize(timeout=300)
    def total_students_by_program(
        self,
        program_code : str
    ) -> int :
        """
        Returns the total number of students under a program.
        """

        res = execute_query(
            query = (
                f"SELECT programcode, COUNT(programcode) " 
                f"FROM {self.table_name} "
                f"WHERE programcode = %s GROUP BY programcode"
            ),
            params = (program_code,),
            fetch = FetchMode.ONE
        )

        return 0 if res is None else res[1]

    def students_info(
        self,
        id : str
    ) -> dict[int | str] :
        """
        Returns the complete details of a student record along with
        the program name, college code, and college name that the student
        is under.
        """

        return execute_query(
            query = (
                "SELECT s.id, s.firstname, s.lastname, s.gender, "
                "s.yearlevel, s.programcode, s.image, p.name AS programname, "
                "c.code AS collegecode, c.name AS collegename "
                "FROM students as s "
                "LEFT JOIN programs as p ON s.programcode = p.code "
                "LEFT JOIN colleges as c ON c.code = p.collegecode "
                "WHERE s.id = %s" 
            ),
            params = (id,),
            fetch = FetchMode.ONE,
            as_dict = True
        )

    def get_image_path(
        self,
        id : str
    ) -> str | None :
        """
        Returns the image path for a student.
        """

        res =  execute_query(
            query = (
                "SELECT s.image "
                "FROM students as s "
                "WHERE s.id = %s" 
            ),
            params = (id,),
            fetch = FetchMode.ONE
        )

        return res[0] if res is not None else res

    def delete_avatar(self, id: str):
        """
        Delete student's image
        """
        self.general_cache_clear()
        execute_query(
            query=(
                f"UPDATE {self.table_name} "
                "SET image = NULL "
                f"WHERE {self.primary} = %s"
            ),
            params=(id,)
        )

std_table : StudentsModel = StudentsModel(
    table_name="students",
    primary="id",
    columns=["id", "firstname", "lastname", "gender", "yearlevel", "programcode", "image"]
)