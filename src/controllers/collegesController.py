from flask import Blueprint, render_template

colleges_bp = Blueprint("colleges", __name__)

@colleges_bp.route("/colleges")
def index():
    return render_template("colleges.html", active_page = 'colleges', header_var='College')