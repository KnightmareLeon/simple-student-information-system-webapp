from .DatabaseConnection import DatabaseConnection
from .BaseTableModel import BaseTableModel

class CollegesModel(BaseTableModel):

    _table_name : str = "colleges"
    _primary : str = "Code"
    @staticmethod
    def getRecords():

        return [
            {'Code' : 'CCS', 'Name' : 'College of Computer Studies'},
            {'Code' : 'COE', 'Name' : 'College of Engineering'},
    ]