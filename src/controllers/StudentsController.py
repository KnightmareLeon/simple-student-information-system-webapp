from flask import Blueprint, Response, jsonify, render_template, request
from flask_login import login_required

from src.models.StudentsModel import std_table
from src.models.ProgramsModel import prg_table

from src.services.Supabase import supabase, get_img_url

students_bp = Blueprint("students", __name__)

@students_bp.route("/students")
@login_required
def index() -> str:
    reqPKeys = prg_table.get_all_pkeys()
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
        column_name = column_name.replace(" ", "").lower()
    else:
        column_name = std_table.primary

    records = std_table.get_filtered_records(
        search_value=search_value,
        sort_column=column_name,
        sort_dir=order_dir,
        limit=length,
        offset=start
    )

    total_filtered_records = std_table.get_total_filtered_records(search_value=search_value)

    for r in records:
        r["actions"] = render_template("partials/_row_buttons_stds.html", key=r["id"])
        r["image"] = get_img_url(r['image'])

    total_records = std_table.get_total()

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_filtered_records,
        "data": records
    })

@students_bp.route("/students", methods=["POST"])
@login_required
def add_student() -> Response:
    id = request.form.get("addID")
    fname = request.form.get("addFirstName")
    lname = request.form.get("addLastName")
    gender = request.form.get("addGender")
    yLevel = request.form.get("addYearLevel")
    program_code = request.form.get("addForeignProgramCode")
    image_file = request.files.get("addStudentImage")

    if std_table.record_exists("id", id):
        return jsonify({"status": "error", "message": f"ID {id} already exists!"}), 409

    image_path = None

    if image_file and image_file.filename != "":
        filename = image_file.filename

        if "." not in filename:
            return jsonify({"status": "error", "message": "Invalid image filename"}), 400

        ext = image_file.filename.rsplit(".", 1)[1].lower()

        if ext not in ("jpg", "jpeg", "png"):
            return jsonify({"status": "error", "message": "Only JPG and PNG allowed"}), 400
        new_filename = f"{id}.{ext}"

        img_bytes = image_file.read()

        supabase.storage.from_("images").upload(
            path=new_filename,
            file=img_bytes,
            file_options={"content-type": image_file.mimetype}
        )

        image_path = new_filename

    try:
        new_data = {
            "id" : id,
            "firstname" : fname,
            "lastname" : lname,
            "gender" : gender,
            "yearlevel" : yLevel,
            "programcode" : program_code,
            "image" : image_path
            }
        std_table.create(new_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "status": "error",
            "message": f"An error occurred when adding student '{fname} {lname}' with ID Number {id}."
        }), 500

    return jsonify({
        "status": "success",
        "message": f"Student '{fname} {lname}' with ID Number {id} added successfully!"
    }), 201

@students_bp.route("/students/<string:id>", methods=["DELETE"])
@login_required
def delete_student(id : str) -> Response:
    try:
        img_path = std_table.get_image_path(id)
        if img_path is not None:
            supabase.storage.from_("images").remove([img_path])
        std_table.delete(id)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
                "status": "error",
                "message": "Student record deletion failed."
            }), 500

    return jsonify({
            "status": "success",
            "message": f"Student with ID number '{id}' deleted successfully!"
        }), 200

@students_bp.route("/students/<string:code>", methods=["GET"])
@login_required
def get_edit_info(code) -> Response:
    try:
        record_data = std_table.get_record(code)
        record_data['image'] = get_img_url(record_data['image'], timeout=5000)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
                "status" : "error",
                "message" : "Error getting student data for editing."
            })
    return jsonify({
            "status" : "success", 
            "data" : record_data
        })

@students_bp.route("/students", methods=["PUT"])
@login_required
def edit_student() -> Response:
    orig_id = request.form.get("editOriginalID")
    orig_img_path = std_table.get_image_path(orig_id)
    id = request.form.get("editID")
    fname = request.form.get("editFirstName")
    lname = request.form.get("editLastName")
    gender = request.form.get("editGender")
    yLevel = request.form.get("editYearLevel")
    program_code = request.form.get("editForeignProgramCode")
    image_file = request.files.get("editStudentImage")

    if std_table.record_exists("id", id) and id != orig_id:
        return jsonify({"status": "error", "message": f"ID {id} already exists"}), 409

    image_path = None

    if image_file and image_file.filename != "":
        filename = image_file.filename

        if "." not in filename:
            return jsonify({"status": "error", "message": "Invalid image filename"}), 400

        ext = image_file.filename.rsplit(".", 1)[1].lower()

        if ext not in ("jpg", "jpeg", "png"):
            return jsonify({"status": "error", "message": "Only JPG and PNG allowed"}), 400
        image_path = f"{id}.{ext}"

        if orig_img_path is not None:
            supabase.storage.from_("images").remove([orig_img_path])

        img_bytes = image_file.read()

        supabase.storage.from_("images").upload(
            path=image_path,
            file=img_bytes,
            file_options={"content-type": image_file.mimetype}
        )

    if id != orig_id and orig_img_path is not None and image_path is None:

        ext = orig_img_path.rsplit(".", 1)[1].lower()
        image_path = f"{id}.{ext}"

        print(image_path)
        print(orig_img_path)
        supabase.storage.from_("images").move(
            orig_img_path,
            image_path
        )

    try:
        new_data = {
            "id" : id,
            "firstname" : fname,
            "lastname" : lname,
            "gender" : gender,
            "yearlevel" : yLevel,
            "programcode" : program_code,
            "image" : image_path if image_path is not None else orig_img_path
        }
        
        std_table.update(orig_id, new_data)
    except Exception as e:
        return jsonify({
                "status": "error",
                "message": f"An error occurred when updating student '{fname} {lname}' with ID Number {id}."
            })

    return jsonify({
            "status": "success",
            "message": f"Student '{fname} {lname}' with ID Number {id} updated successfully!"
        })

@students_bp.route("/students/dup", methods=["GET"])
@login_required
def check_duplicates():
    id = request.args.get('id', '').strip()
    exists = std_table.record_exists("ID", id)
    return  jsonify({'exists' : exists}), 200

@students_bp.route("/students/info/<string:id>", methods=["GET"])
@login_required
def get_students_info(id : str):
    try:
        student_data = std_table.students_info(id)
        student_data['image'] = get_img_url(student_data['image'])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "status" : "error",
            "message" : f"An error occured when getting the students's data/information"
        }), 404
    return jsonify({"status" : "success", "data": student_data}), 200

@students_bp.route("/students/avatar/<string:id>", methods=["DELETE"])
@login_required
def delete_avatar(id: str):
    try:
        img_path: str = std_table.get_image_path(id)
        if img_path is not None:
            supabase.storage.from_("images").remove([img_path])
            std_table.delete_avatar(id)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
                "status": "error",
                "message": "Student avatar deletion failed."
            }), 500

    return jsonify({
            "status": "success",
            "message": f"Student with ID number '{id}' image deleted successfully!"
        }), 200
