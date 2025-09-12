from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template("dashboard/index.html", active_page = "dashboard", total_stds=50, total_prgs=5, total_clgs=2)