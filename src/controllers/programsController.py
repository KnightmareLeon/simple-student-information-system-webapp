from flask import Blueprint, Response, flash, redirect, render_template, request, jsonify
from flask_login import login_required

from src.models.ProgramsModel import ProgramsModel
from src.models.CollegesModel import CollegesModel

programs_bp = Blueprint("programs", __name__)

@programs_bp.route("/programs")
@login_required
def index() -> str:
    reqPKeys = CollegesModel.get_aLL_pkeys()
    return render_template("programs/index.html", active_page = 'programs', header_var='Program', reqPKeys=reqPKeys)

@programs_bp.route("/programs/data", methods=["POST"])
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
        column_name = ProgramsModel.get_primary_key()

    records = ProgramsModel.get_filtered_records(
        search_value=search_value,
        sort_column=column_name,
        sort_dir=order_dir,
        limit=length,
        offset=start
    )

    total_filtered_records = ProgramsModel.get_total_filtered_records(search_value=search_value)

    for r in records:
        r["actions"] = render_template("partials/_row_buttons.html", key=r["Code"])

    total_records = ProgramsModel.get_total()

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_filtered_records,
        "data": records
    })

@programs_bp.route("/programs/add", methods=["POST"])
@login_required
def add_program() -> Response:
    code = request.form.get("addProgramPrimaryCode")
    name = request.form.get("addProgramName")
    college_code = request.form.get("addForeignCollegeCode")

    code_dup = ProgramsModel.record_exists("Code", code)
    name_dup =  ProgramsModel.record_exists("Name", name)
    if code_dup or name_dup:
        message = []
        message.append(f"Program code '{code}' already exists! " if code_dup else "")
        message.append(f"Program name '{name}' already exists!" if name_dup else "")
        return jsonify({"status": "error", "message": " , ".join(message)})
    
    try:
        new_data = {"Code" : code, "Name" : name, "CollegeCode" : college_code}
        ProgramsModel.create(new_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": f"An error occurred when adding program '{code}'."})

    return jsonify({"status": "success", "message": f"Program '{name}' added successfully!"})

@programs_bp.route("/programs/delete/<string:code>", methods=["POST"])
@login_required
def delete_program(code : str) -> Response:
    try:
        ProgramsModel.delete(code)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Program record deletion failed."}), 404

    return jsonify({"status": "success", "message": f"Program '{code}' deleted successfully!"})

@programs_bp.route("/programs/get_edit_info/<string:code>")
@login_required
def get_edit_info(code) -> Response:
    try:
        recordData = ProgramsModel.get_record(code)
    except Exception as e:
        return jsonify(status="error", message="Error getting program data for editing.")
    return jsonify(status="success", data=recordData)

@programs_bp.route("/programs/edit", methods=["POST"])
@login_required
def edit_program() -> Response:
    try:
        orig_code = request.form.get("editOriginalProgramCode")
        orig_name = ProgramsModel.get_record(orig_code)["Name"]
        code = request.form.get("editProgramPrimaryCode")
        name = request.form.get("editProgramName")
        college_code = request.form.get("editForeignCollegeCode")

        code_dup = ProgramsModel.record_exists("Code", code)
        name_dup =  ProgramsModel.record_exists("Name", name)
        if (code_dup and orig_code != code )  or ( name_dup and orig_name != name):
            message = []
            message.append(f"Program code '{code}' already exists! " if code_dup and orig_code != code else "")
            message.append(f"Program name '{name}' already exists!" if name_dup and orig_name != name else "")
            return jsonify({"status": "error", "message": " , ".join(message)})
    

        new_data = {"Code" : code, "Name" : name, "CollegeCode" : college_code}
        ProgramsModel.update(orig_code, new_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": f"An error occurred when updating program '{code}'."})

    return jsonify({"status": "success", "message": f"Program '{name}' updated successfully!"})

@programs_bp.route("/programs/check_duplicates")
@login_required
def check_duplicates():
    code = request.args.get('code', '').strip()
    name = request.args.get('name', '').strip()
    exists_code = ProgramsModel.record_exists("Code", code)
    exists_name = ProgramsModel.record_exists("Name", name)
    return  jsonify({
            'exists_code': exists_code,
            'exists_name': exists_name
        })