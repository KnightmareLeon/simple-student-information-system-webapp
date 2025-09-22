from flask import Blueprint, Response, jsonify, render_template, request
from src.models.CollegesModel import CollegesModel

colleges_bp = Blueprint("colleges", __name__)

@colleges_bp.route("/colleges")
def index() -> str:
    return render_template("colleges/index.html", active_page = 'colleges', header_var='College')

@colleges_bp.route("/colleges/data", methods=["POST"])
def data() -> Response:
    draw = int(request.form.get("draw", 1))
    start = int(request.form.get("start", 0))
    length = int(request.form.get("length", 10))
    search_value = request.form.get("search[value]", "")
    order_column_index = request.form.get("order[0][column]")
    order_dir = request.form.get("order[0][dir]", "asc")
    column_name = request.form.get(f"columns[{order_column_index}][data]").replace(" ", "")

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
def add_college() -> Response:
    code = request.form.get("recordCollegePrimaryCode")
    name = request.form.get("recordCollegeName")

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
        return jsonify({"status": "error", "message": f"An error occurred adding College {code}."})
    return jsonify({"status": "success", "message": f"College '{code}' added successfully!"})

@colleges_bp.route("/colleges/delete/<string:code>", methods=["POST"])
def delete_college(code : str) -> Response:
    try:
        CollegesModel.delete(code)
    except Exception as e:
        return jsonify({"status": "error", "message": "College record deletion failed."}), 404

    return jsonify({"status": "success", "message": f"College '{code}' deleted successfully!"})

@colleges_bp.route("/colleges/check_duplicates")
def check_duplicates() -> Response:
    code = request.args.get('code', '').strip()
    name = request.args.get('name', '').strip()
    exists_code = CollegesModel.record_exists("Code", code)
    exists_name = CollegesModel.record_exists("Name", name)
    return  jsonify({
            'exists_code': exists_code,
            'exists_name': exists_name
        })