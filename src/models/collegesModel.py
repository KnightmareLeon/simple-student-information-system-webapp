from .DatabaseConnection import DatabaseConnection
from .BaseTableModel import BaseTableModel

class CollegesModel(BaseTableModel):

    _table_name : str = "colleges"
    _primary : str = "Code"

    @classmethod
    def _create_table(cls):
        from dotenv import load_dotenv
        import os
        try:

            cursor = DatabaseConnection.get_connection().cursor()
            load_dotenv()
            user = os.getenv("USER")
            query = (
                "CREATE TABLE IF NOT EXISTS public.colleges\n"
                "(\n"
                "    \"Code\" character varying(5) COLLATE pg_catalog.\"default\" NOT NULL,\n"
                "    \"Name\" character varying(100) COLLATE pg_catalog.\"default\" NOT NULL,\n"
                "    CONSTRAINT colleges_pkey PRIMARY KEY (\"Code\"),\n"
                "    CONSTRAINT unique_college_name UNIQUE (\"Name\")\n"
                ")\n"
                "TABLESPACE pg_default;\n"
                "ALTER TABLE IF EXISTS public.colleges\n"
                f"    OWNER to {user};"
            )
            cursor.execute(query)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def college_info(
        cls,
        code : str
    ) -> dict[int | str] :
        """
        Returns the complete details of a college record along with
        the total programs and students under it.
        """
        result = None

        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            query = (
                "SELECT "
                "c.\"Code\", c.\"Name\", "
                "COUNT(DISTINCT p.\"Code\") as \"TotalPrograms\", "
                "COUNT(s.\"ID\") as \"TotalStudents\" "
                "FROM colleges as c "
                "LEFT JOIN programs as p on c.\"Code\" = p.\"CollegeCode\" "
                "LEFT JOIN students as s on p.\"Code\" = s.\"ProgramCode\" "
                "WHERE c.\"Code\" = %s "
                "GROUP BY c.\"Code\", c.\"Name\" "
            )
            cursor.execute(query, (code,))
            
            result = cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result