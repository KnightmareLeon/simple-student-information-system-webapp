from src.models.DatabaseConnection import DatabaseConnection
from .BaseTableModel import BaseTableModel

class ProgramsModel(BaseTableModel):

    _table_name = "programs"
    _primary = "Code"

    @classmethod
    def _create_table(cls):
        from dotenv import load_dotenv
        import os
        try:

            cursor = DatabaseConnection.get_connection().cursor()
            load_dotenv()
            user = os.getenv("USER")
            query = (
                "CREATE TABLE IF NOT EXISTS public.programs\n"
                "(\n"
                "    \"Code\" character varying(20) COLLATE pg_catalog.\"default\" NOT NULL,\n"
                "    \"Name\" character varying(100) COLLATE pg_catalog.\"default\" NOT NULL,\n"
                "    \"CollegeCode\" character varying(5) COLLATE pg_catalog.\"default\",\n"
                "    CONSTRAINT programs_pkey PRIMARY KEY (\"Code\"),\n"
                "    CONSTRAINT unique_program_name UNIQUE (\"Name\"),\n"
                "    CONSTRAINT programs_fkey FOREIGN KEY (\"CollegeCode\")\n"
                "        REFERENCES public.colleges (\"Code\") MATCH SIMPLE\n"
                "        ON UPDATE CASCADE\n"
                "        ON DELETE SET NULL\n"
                ")\n"
                "TABLESPACE pg_default;\n"
                "ALTER TABLE IF EXISTS public.programs\n"
                f"    OWNER to {user};"
            )
            cursor.execute(query)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def total_programs_by_college(
        cls,
        college_code : str
    ) -> int :
        """
        Returns the total number of programs under a college.
        """
        result = 0

        try:
            cursor = DatabaseConnection.get_connection().cursor()
            query = f"SELECT \"CollegeCode\", COUNT(\"CollegeCode\") FROM {cls.get_table_name()} WHERE \"CollegeCode\" = %s GROUP BY \"CollegeCode\""
            cursor.execute(query, (college_code,))
            
            result = cursor.fetchone()
            if not result:
                result = 0
            else:
                result = result[1]
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result
    
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

        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            query = (
                "SELECT "
                "p.\"Code\", p.\"Name\", p.\"CollegeCode\", "
                "c.\"Name\" AS \"CollegeName\", "
                "COUNT(s.\"ProgramCode\") AS \"TotalStudents\""
                "FROM programs as p "
                "LEFT JOIN colleges as c ON p.\"CollegeCode\" = c.\"Code\" "
                "LEFT JOIN students as s ON p.\"Code\" = s.\"ProgramCode\" "
                "WHERE p.\"Code\" = %s "
                "GROUP BY p.\"Code\", p.\"Name\", p.\"CollegeCode\", c.\"Name\"" 
            )
            cursor.execute(query, (code,))
            
            result = cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result