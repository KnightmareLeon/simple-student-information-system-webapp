from flask import Blueprint, render_template

students_bp = Blueprint("students", __name__)

@students_bp.route("/students")
def index():
    return render_template("students.html", active_page = 'students', header_var='Student')