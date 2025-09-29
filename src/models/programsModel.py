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