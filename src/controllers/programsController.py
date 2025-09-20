from flask import Blueprint, render_template
from src.models.ProgramsModel import ProgramsModel
from src.models.CollegesModel import CollegesModel
programs_bp = Blueprint("programs", __name__)

@programs_bp.route("/programs")
def index():
    records = ProgramsModel.get_aLL_records()
    reqPKeys = CollegesModel.get_aLL_pkeys()
    return render_template("programs/index.html", active_page = 'programs', header_var='Program', records=records, reqPKeys=reqPKeys)