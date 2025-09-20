from flask import Blueprint, render_template
from src.models.StudentsModel import StudentsModel
from src.models.ProgramsModel import ProgramsModel

students_bp = Blueprint("students", __name__)

@students_bp.route("/students")
def index():
    records = StudentsModel.get_aLL_records()
    reqPKeys = ProgramsModel.get_aLL_pkeys()
    return render_template("students/index.html", active_page = 'students', header_var='Student', records=records, reqPKeys=reqPKeys)