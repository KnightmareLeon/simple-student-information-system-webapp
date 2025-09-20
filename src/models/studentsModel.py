from .BaseTableModel import BaseTableModel

class StudentsModel(BaseTableModel):

    _table_name = "students"
    _primary = "ID"