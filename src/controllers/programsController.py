from flask import Blueprint, render_template
from src.models.programsModel import ProgramsModel

programs_bp = Blueprint("programs", __name__)
current_page : int = 1
records : list[dict] = []

@programs_bp.route("/programs")
def index():
    global records
    if(len(records) == 0):
        records = ProgramsModel.getRecords()
    return render_template("programs.html", active_page = 'programs', header_var='Program', records=records)