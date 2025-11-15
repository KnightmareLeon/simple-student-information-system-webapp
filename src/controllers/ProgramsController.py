from flask import Blueprint, Response, render_template, request, jsonify
from flask_login import login_required

from src.models.ProgramsModel import prg_table
from src.models.CollegesModel import col_table

programs_bp = Blueprint("programs", __name__)

@programs_bp.route("/programs")
@login_required
def index() -> str:
    reqPKeys = col_table.get_all_pkeys()
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
        column_name = column_name.replace(" ", "").lower()
    else:
        column_name = prg_table.primary

    records = prg_table.get_filtered_records(
        search_value=search_value,
        sort_column=column_name,
        sort_dir=order_dir,
        limit=length,
        offset=start
    )

    total_filtered_records = prg_table.get_total_filtered_records(search_value=search_value)

    for r in records:
        r["actions"] = render_template("partials/_row_buttons.html", key=r["code"])

    total_records = prg_table.get_total()

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_filtered_records,
        "data": records
    })

@programs_bp.route("/programs", methods=["POST"])
@login_required
def add_program() -> Response:
    code = request.form.get("addProgramPrimaryCode")
    name = request.form.get("addProgramName")
    college_code = request.form.get("addForeignCollegeCode")

    code_dup = prg_table.record_exists("code", code)
    name_dup =  prg_table.record_exists("name", name)
    if code_dup or name_dup:
        message = []
        message.append(f"Program code '{code}' already exists! " if code_dup else "")
        message.append(f"Program name '{name}' already exists!" if name_dup else "")
        return jsonify({"status": "error", "message": " , ".join(message)}), 409
    
    try:
        new_data = {"Code" : code, "name" : name, "collegecode" : college_code}
        prg_table.create(new_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": f"An error occurred when adding program '{code}'."}), 500

    return jsonify({"status": "success", "message": f"Program '{name}' added successfully!"}), 201

@programs_bp.route("/programs/<string:code>", methods=["DELETE"])
@login_required
def delete_program(code : str) -> Response:
    try:
        prg_table.delete(code)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Program record deletion failed."}), 500

    return jsonify({"status": "success", "message": f"Program '{code}' deleted successfully!"}), 200

@programs_bp.route("/programs/<string:code>", methods=["GET"])
@login_required
def get_edit_info(code : str) -> Response:
    try:
        recordData = prg_table.get_record(code)
    except Exception as e:
        return jsonify(status="error", message="Error getting program data for editing."), 500
    return jsonify({"status" : "success", "data" : recordData}), 200

@programs_bp.route("/programs", methods=["PUT"])
@login_required
def edit_program() -> Response:
    try:
        orig_code = request.form.get("editOriginalProgramCode")
        orig_name = prg_table.get_record(orig_code)["name"]
        code = request.form.get("editProgramPrimaryCode")
        name = request.form.get("editProgramName")
        college_code = request.form.get("editForeignCollegeCode")

        code_dup = prg_table.record_exists("code", code)
        name_dup =  prg_table.record_exists("name", name)
        if (code_dup and orig_code != code )  or ( name_dup and orig_name != name):
            message = []
            message.append(f"Program code '{code}' already exists! " if code_dup and orig_code != code else "")
            message.append(f"Program name '{name}' already exists!" if name_dup and orig_name != name else "")
            return jsonify({"status": "error", "message": " , ".join(message)}), 409
    

        new_data = {"code" : code, "name" : name, "collegecode" : college_code}
        prg_table.update(orig_code, new_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": f"An error occurred when updating program '{code}'."}), 500

    return jsonify({"status": "success", "message": f"Program '{name}' updated successfully!"}), 200

@programs_bp.route("/programs/dup", methods=["GET"])
@login_required
def check_duplicates() -> Response:
    code = request.args.get('code', '').strip()
    name = request.args.get('name', '').strip()
    exists_code = prg_table.record_exists("code", code)
    exists_name = prg_table.record_exists("name", name)
    return  jsonify({
            'exists_code': exists_code,
            'exists_name': exists_name
        }), 200

@programs_bp.route("/programs/info/<string:code>", methods=["GET"])
@login_required
def get_program_info(code : str):
    try:
        program_data = prg_table.program_info(code)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status" : "error", "message" : f"An error occured when getting the program's data/information"}), 404
    return jsonify({"status" : "success", "data": program_data})