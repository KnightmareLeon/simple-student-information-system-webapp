from flask import Blueprint, render_template

programs_bp = Blueprint("programs", __name__)

@programs_bp.route("/programs")
def index():
    return render_template("programs.html", active_page = 'programs', header_var='Program')