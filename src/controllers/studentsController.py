from flask import Blueprint, Response, jsonify, render_template, request, url_for
from flask_login import login_required

from src.models.StudentsModel import StudentsModel
from src.models.ProgramsModel import ProgramsModel

students_bp = Blueprint("students", __name__)

@students_bp.route("/students")
@login_required
def index() -> str:
    reqPKeys = ProgramsModel.get_aLL_pkeys()
    return render_template("students/index.html", active_page = 'students', header_var='Student', reqPKeys=reqPKeys)

@students_bp.route("/students/data", methods=["POST"])
@login_required
def data() -> Response:
    draw = int(request.form.get("draw", 1))
    start = int(request.form.get("start", 0))
    length = int(request.form.get("length", 10))
    search_value = request.form.get("search[value]", "")
    order_column_index = request.form.get("order[0][column]")
    order_dir = request.form.get("order[0][dir]", "asc")
    column_name = request.form.get(f"columns[{order_column_index}][data]")


    if column_name:
        column_name = column_name.replace(" ", "")
    else:
        column_name = StudentsModel.get_primary_key()

    records = StudentsModel.get_filtered_records(
        search_value=search_value,
        sort_column=column_name,
        sort_dir=order_dir,
        limit=length,
        offset=start
    )

    total_filtered_records = StudentsModel.get_total_filtered_records(search_value=search_value)

    for r in records:
        r["actions"] = render_template("partials/_row_buttons.html", key=r["ID"])

    total_records = StudentsModel.get_total()

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_filtered_records,
        "data": records
    })

@students_bp.route("/students/add", methods=["POST"])
@login_required
def add_student() -> Response:
    id = request.form.get("addID")
    fname = request.form.get("addFirstName")
    lname = request.form.get("addLastName")
    gender = request.form.get("addGender")
    yLevel = request.form.get("addYearLevel")
    program_code = request.form.get("addForeignProgramCode")

    if StudentsModel.record_exists("ID", id):
        return jsonify({"status": "error", "message": f"ID {id} already exists"})

    try:
        new_data = {"ID" : id, "FirstName" : fname, "LastName" : lname, "Gender" : gender, "YearLevel" : yLevel, "ProgramCode" : program_code}
        StudentsModel.create(new_data)
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred when adding student '{fname} {lname}' with ID Number {id}."})

    return jsonify({"status": "success", "message": f"Student '{fname} {lname}' with ID Number {id} added successfully!"})

@students_bp.route("/students/delete/<string:id>", methods=["POST"])
@login_required
def delete_college(id : str) -> Response:
    try:
        StudentsModel.delete(id)
    except Exception as e:
        return jsonify({"status": "error", "message": "Student record deletion failed."}), 404

    return jsonify({"status": "success", "message": f"Student with ID number '{id}' deleted successfully!"})

@students_bp.route("/students/get_edit_info/<string:code>")
@login_required
def get_edit_info(code) -> Response:
    try:
        recordData = StudentsModel.get_record(code)
    except Exception as e:
        return jsonify(status="error", message="Error getting student data for editing.")
    return jsonify(status="success", data=recordData)

@students_bp.route("/students/check_duplicates")
@login_required
def check_duplicates():
    id = request.args.get('id', '').strip()
    exists = StudentsModel.record_exists("ID", id)
    return  jsonify({'exists' : exists})