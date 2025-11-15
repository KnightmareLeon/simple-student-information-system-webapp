from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models.User import User
from src.models.CollegesModel import col_table
from src. models.ProgramsModel import prg_table
from src.models.StudentsModel import std_table

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    return render_template(
        "dashboard/index.html",
        username = User.get_by_id(current_user.get_id()).username,
        active_page = "dashboard",
        total_stds=std_table.get_total(),
        total_prgs=prg_table.get_total(),
        total_clgs=col_table.get_total()
    )