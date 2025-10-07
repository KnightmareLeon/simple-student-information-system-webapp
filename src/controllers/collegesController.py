from flask import Blueprint, Response, jsonify, render_template, request
from flask_login import login_required

from src.models.CollegesModel import CollegesModel
from src.models.ProgramsModel import ProgramsModel

colleges_bp = Blueprint("colleges", __name__)

@colleges_bp.route("/colleges")
@login_required
def index() -> str:
    return render_template("colleges/index.html", active_page = 'colleges', header_var='College')

@colleges_bp.route("/colleges/data", methods=["POST"])
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
        column_name = CollegesModel.get_primary_key()

    records = CollegesModel.get_filtered_records(
        search_value=search_value,
        sort_column=column_name,
        sort_dir=order_dir,
        limit=length,
        offset=start
    )

    total_filtered_records = CollegesModel.get_total_filtered_records(search_value=search_value)

    for r in records:
        r["actions"] = render_template("partials/_row_buttons.html", key=r["Code"])
    total_records = CollegesModel.get_total()

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_filtered_records,
        "data": records
    })

@colleges_bp.route("/colleges/add", methods=["POST"])
@login_required
def add_college() -> Response:
    code = request.form.get("addCollegePrimaryCode")
    name = request.form.get("addCollegeName")

    code_dup = CollegesModel.record_exists("Code", code)
    name_dup =  CollegesModel.record_exists("Name", name)
    if code_dup or name_dup:
        message = []
        message.append(f"College code '{code}' already exists! " if code_dup else "")
        message.append(f"College name '{name}' already exists!" if name_dup else "")
        return jsonify({"status": "error", "message": " , ".join(message)})
    try:
        new_data = {"Code" : code, "Name" : name}
        CollegesModel.create(new_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": f"An error occurred adding College {code}."})
    return jsonify({"status": "success", "message": f"College '{code}' added successfully!"})

@colleges_bp.route("/colleges/delete/<string:code>", methods=["POST"])
@login_required
def delete_college(code : str) -> Response:
    try:
        CollegesModel.delete(code)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "College record deletion failed."}), 404

    return jsonify({"status": "success", "message": f"College '{code}' deleted successfully!"})

@colleges_bp.route("/colleges/get_edit_info/<string:code>")
@login_required
def get_edit_info(code) -> Response:
    try:
        recordData = CollegesModel.get_record(code)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(status="error", message="Error getting college data for editing.")
    return jsonify(status="success", data=recordData)

@colleges_bp.route("/colleges/update", methods=["POST"])
@login_required
def edit_college() -> Response:
    try:
        orig_code = request.form.get("editOriginalCollegeCode")
        orig_name = CollegesModel.get_record(orig_code)["Name"]
        code = request.form.get("editCollegePrimaryCode")
        name = request.form.get("editCollegeName")

        code_dup = CollegesModel.record_exists("Code", code)
        name_dup =  CollegesModel.record_exists("Name", name)
        if (code_dup and orig_code != code ) or ( name_dup and orig_name != name):
            message = []
            message.append(f"College code '{code}' already exists! " if code_dup and orig_code != code else "")
            message.append(f"College name '{name}' already exists!" if name_dup  and orig_name != name else "")
            return jsonify({"status": "error", "message": " , ".join(message)})

        new_data = {"Code" : code, "Name" : name}
        CollegesModel.update(orig_code, new_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": f"An error occurred updating college."})
    return jsonify({"status": "success", "message": f"College '{code}' updated successfully!"})

@colleges_bp.route("/colleges/check_duplicates")
@login_required
def check_duplicates() -> Response:
    code = request.args.get('code', '').strip()
    name = request.args.get('name', '').strip()
    exists_code = CollegesModel.record_exists("Code", code)
    exists_name = CollegesModel.record_exists("Name", name)
    return  jsonify({
            'exists_code': exists_code,
            'exists_name': exists_name
        })

@colleges_bp.route("/colleges/info/<string:code>", methods=["GET"])
@login_required
def get_college_info(code : str):
    try:
        college_data = CollegesModel.college_info(code)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status" : "error", "message" : f"An error occured when getting the program's data/information"}), 404
    return jsonify({"status" : "success", "data": college_data})