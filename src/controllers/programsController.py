from flask import Blueprint, Response, flash, redirect, render_template, request, jsonify, url_for
from src.models.ProgramsModel import ProgramsModel
from src.models.CollegesModel import CollegesModel

programs_bp = Blueprint("programs", __name__)

@programs_bp.route("/programs")
def index() -> str:
    reqPKeys = CollegesModel.get_aLL_pkeys()
    return render_template("programs/index.html", active_page = 'programs', header_var='Program', reqPKeys=reqPKeys)

@programs_bp.route("/programs/data", methods=["POST"])
def data() -> Response:
    draw = int(request.form.get("draw", 1))
    start = int(request.form.get("start", 0))
    length = int(request.form.get("length", 10))
    search_value = request.form.get("search[value]", "")
    order_column_index = request.form.get("order[0][column]")
    order_dir = request.form.get("order[0][dir]", "asc")
    column_name = request.form.get(f"columns[{order_column_index}][data]").replace(" ", "")

    records = ProgramsModel.get_filtered_records(
        search_value=search_value,
        sort_column=column_name,
        sort_dir=order_dir,
        limit=length,
        offset=start
    )

    total_filtered_records = ProgramsModel.get_total_filtered_records(search_value=search_value)

    reqPKeys = CollegesModel.get_aLL_pkeys()

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
def add_program() -> Response:
    code = request.form.get("recordProgramPrimaryCode")
    name = request.form.get("recordProgramName")
    college_code = request.form.get("recordForeignCollegeCode")

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
        return jsonify({"status": "error", "message": f"An error occurred when adding program '{code}'."})

    return jsonify({"status": "success", "message": f"Program '{name}' added successfully!"})

@programs_bp.route("/programs/delete/<string:code>", methods=["POST"])
def delete_program(code : str) -> Response:
    try:
        ProgramsModel.delete(code)
    except Exception as e:
        return jsonify({"status": "error", "message": "Program record deletion failed."}), 404

    return jsonify({"status": "success", "message": f"Program '{code}' deleted successfully!"})

@programs_bp.route("/programs/<string:code>/edit-form")
def edit_form(code):
    return render_template(
        "programs/partials/_form.html",
        form_id="editRecordForm",
        form_action=url_for("programs.update_program", code=code)
    )

@programs_bp.route("/programs/check_duplicates")
def check_duplicates():
    code = request.args.get('code', '').strip()
    name = request.args.get('name', '').strip()
    exists_code = ProgramsModel.record_exists("Code", code)
    exists_name = ProgramsModel.record_exists("Name", name)
    return  jsonify({
            'exists_code': exists_code,
            'exists_name': exists_name
        })