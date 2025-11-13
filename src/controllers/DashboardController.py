from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models.User import User
from src.models.CollegesModel import CollegesModel
from src. models.ProgramsModel import ProgramsModel
from src.models.StudentsModel import StudentsModel

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    return render_template(
        "dashboard/index.html",
        username = User.get_by_id(current_user.get_id()).username,
        active_page = "dashboard",
        total_stds=StudentsModel.get_total(),
        total_prgs=ProgramsModel.get_total(),
        total_clgs=CollegesModel.get_total()
    )