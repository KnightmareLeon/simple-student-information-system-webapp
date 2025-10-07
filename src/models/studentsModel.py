from .DatabaseConnection import DatabaseConnection
from .BaseTableModel import BaseTableModel

class StudentsModel(BaseTableModel):

    _table_name = "students"
    _primary = "ID"

    @classmethod
    def total_students_by_program(
        cls,
        program_code : str
    ) -> int :
        """
        Returns the total number of students under a program.
        """
        result = 0

        try:
            cursor = DatabaseConnection.get_connection().cursor()
            query = f"SELECT \"ProgramCode\", COUNT(\"ProgramCode\") FROM {cls.get_table_name()} WHERE \"ProgramCode\" = %s GROUP BY \"ProgramCode\""
            cursor.execute(query, (program_code,))
            
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

        try:
            cursor = DatabaseConnection.get_connection().cursor(cursor_factory=DatabaseConnection.real_dict)
            query = (
                "SELECT s.\"ID\", s.\"FirstName\", s.\"LastName\", s.\"Gender\", "
                "s.\"YearLevel\", s.\"ProgramCode\", p.\"Name\" AS \"ProgramName\", "
                "c.\"Code\" AS \"CollegeCode\", c.\"Name\" AS \"CollegeName\""
                "FROM students as s "
                "LEFT JOIN programs as p ON s.\"ProgramCode\" = p.\"Code\" "
                "LEFT JOIN colleges as c ON c.\"Code\" = p.\"CollegeCode\" "
                "WHERE s.\"ID\" = %s" 
            )
            cursor.execute(query, (id,))
            
            result = cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return result