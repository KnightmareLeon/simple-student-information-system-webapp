from .DatabaseConnection import DatabaseConnection
from .BaseTableModel import BaseTableModel

class CollegesModel(BaseTableModel):

    _table_name : str = "colleges"
    _primary : str = "Code"