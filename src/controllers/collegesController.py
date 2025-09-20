from flask import Blueprint, render_template
from src.models.CollegesModel import CollegesModel

colleges_bp = Blueprint("colleges", __name__)

@colleges_bp.route("/colleges")
def index():
    records = CollegesModel.get_aLL_records()
    return render_template("colleges/index.html", active_page = 'colleges', header_var='College', records=records)