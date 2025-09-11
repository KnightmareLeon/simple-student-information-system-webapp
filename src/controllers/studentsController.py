from flask import Blueprint, render_template
from src.models.studentsModel import StudentsModel

students_bp = Blueprint("students", __name__)
current_page : int = 1
max_page : int = 1
records : list[dict] = []

@students_bp.route("/students")
def index():
    global records
    if(len(records) == 0):
        records = StudentsModel.getRecords()
    return render_template("students/index.html", active_page = 'students', header_var='Student', records=records, current_page=current_page, max_page=max_page)