from src.models.DatabaseConnection import DatabaseConnection
from .BaseTableModel import BaseTableModel

class ProgramsModel(BaseTableModel):

    _table_name = "programs"
    _primary = "Code"

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