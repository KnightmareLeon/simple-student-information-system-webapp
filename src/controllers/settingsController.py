from flask import Blueprint, render_template

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings")
def index():
    return render_template("settings.html", active_page = 'settings')