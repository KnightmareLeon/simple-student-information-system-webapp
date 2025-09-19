from .DatabaseConnection import DatabaseConnection

class CollegesModel():

    @staticmethod
    def getRecords():

        return [
            {'Code' : 'CCS', 'Name' : 'College of Computer Studies'},
            {'Code' : 'COE', 'Name' : 'College of Engineering'},
        ]
    
    @staticmethod
    def get_total_colleges() -> int:
        total = 0
        try:
            cursor = DatabaseConnection.get_connection().cursor()
            cursor.execute("SELECT COUNT(*) FROM colleges;")
            total = cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            cursor.close()
        return