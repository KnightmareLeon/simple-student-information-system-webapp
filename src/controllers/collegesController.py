from flask import Blueprint, render_template
from src.models.collegesModel import CollegesModel

colleges_bp = Blueprint("colleges", __name__)
current_page : int = 1
records : list[dict] = []

@colleges_bp.route("/colleges")
def index():
    global records
    if(len(records) == 0):
        records = CollegesModel.getRecords()
    return render_template("colleges.html", active_page = 'colleges', header_var='College', records=records)