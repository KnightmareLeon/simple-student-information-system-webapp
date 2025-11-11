from .DatabaseConnection import execute_query, FetchMode
from .BaseTableModel import BaseTableModel

class StudentsModel(BaseTableModel):

    _table_name = "students"
    _primary = "id"
    _columns : list[str] = ["id", "firstname", "lastname", "gender", "yearlevel", "programcode"]

    # CREATE TABLE IF NOT EXISTS public.students
    # (
    #     id character(9) COLLATE pg_catalog."default" NOT NULL,
    #     firstname character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #     lastname character varying(100) COLLATE pg_catalog."default" NOT NULL,
    #     gender gender NOT NULL,
    #     yearlevel year_level NOT NULL,
    #     programcode character varying(20) COLLATE pg_catalog."default",
    #     CONSTRAINT students_pkey PRIMARY KEY (id),
    #     CONSTRAINT students_fkey FOREIGN KEY (programcode)
    #         REFERENCES public.programs (code) MATCH SIMPLE
    #         ON UPDATE CASCADE
    #         ON DELETE SET NULL,
    #     CONSTRAINT first_name_format CHECK (firstname::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(firstname::text) <= 100),
    #     CONSTRAINT id_format CHECK (id ~ '^(?:19(?:6[7-9]|[7-9][0-9])|20[0-9]{2}|2100)-(?:000[1-9]|00[1-9][0-9]|0[1-9][0-9]{2}|[1-9][0-9]{3})$'::text),
    #     CONSTRAINT last_name_format CHECK (lastname::text ~ '^[[:alpha:]]+( [[:alpha:]]+)*$'::text AND length(lastname::text) <= 100)
    # )

    @classmethod
    def total_students_by_program(
        cls,
        program_code : str
    ) -> int :
        """
        Returns the total number of students under a program.
        """

        res = execute_query(
            query = (
                f"SELECT programcode, COUNT(programcode) " 
                f"FROM {cls.get_table_name()} "
                f"WHERE programcode = %s GROUP BY programcode"
            ),
            params = (program_code,),
            fetch = FetchMode.ONE
        )

        return 0 if res is None else res[1]

    @classmethod
    def students_info(
        cls,
        id : str
    ) -> dict[int | str] :
        """
        Returns the complete details of a student record along with
        the program name, college code, and college name that the student
        is under.
        """
        result = None

        return execute_query(
            query = (
                "SELECT s.id, s.firstname, s.lastname, s.gender, "
                "s.yearlevel, s.programcode, p.name AS programname, "
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