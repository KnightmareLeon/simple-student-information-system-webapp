//Check Duplicates
$('#addProgramPrimaryCode, #addProgramName').on('blur input', function() {
    let code = $('#addProgramPrimaryCode').val().trim();
    let name = $('#addProgramName').val().trim();
    if (!code && !name) return;

    $.get('/programs/check_duplicates', { code: code, name: name }, function(resp) {
        const $alert = $('#addProgramFormAlert');
        if (resp.exists_code || resp.exists_name) {
            let msg = [];
            if (resp.exists_code) msg.push(`Code '${code}' already exists`);
            if (resp.exists_name) msg.push(`Name '${name}' already exists`);
            $alert.removeClass('d-none alert-success').addClass('alert-danger').text(msg.join(', '));
        } else {
            $alert.addClass('d-none');
        }
    });
});

//Handle Edit Button
$('#ProgramTable').on('click', '.edit-btn', function () {
    const recordId = $(this).data('id');

    $.get(`/programs/get_edit_info/${recordId}`, function (resp) {
        if (resp.status === "success") {
            $('#editOriginalProgramCode').val(resp.data.Code);
            $('#editProgramPrimaryCode').val(resp.data.Code);
            $('#editProgramName').val(resp.data.Name);
            $('select[name=editForeignCollegeCode]').selectpicker('val', resp.data.CollegeCode);
            $('select[name=editForeignCollegeCode]').selectpicker('render');
            $('#editProgramModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
});

//Handle Info Button
$('#ProgramTable').on('click', '.info-btn', function () {
    const programCode = $(this).data('id')
    $.get(`/programs/info/${programCode}`, function(resp){
        if (resp.status === "success") {
            $('#infoProgramCode').text(programCode);
            $('#infoProgramName').text(resp.data.Name);
            $('#infoForeignCollegeCode').text(resp.data.CollegeCode);
            $('#infoForeignCollegeName').text(resp.data.CollegeName);
            $('#infoProgramStudentCount').text(resp.data.TotalStudents);
            $('#infoProgramModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
    
});

let programTable = $('#ProgramTable').DataTable({
    processing: true, 
    serverSide: true, 
    ajax: {
        url: "/programs/data",
        type: "POST"
    },
    columns: [
        { data: "Code" },
        { data: "Name" },
        { data: "CollegeCode" },
        { data: "actions", orderable: false, searchable: false }
    ]
});

setupTableModal(
    '#addProgramForm',
    '#addProgramModal', 
    '#addProgramFormAlert',
    '#ProgramTable',
    'addForeignCollegeCode'
);

setupDeleteHandler(
    '#ProgramTable',
    'programs'
);

setupEditSubmit(
    '#editProgramForm',
    '#ProgramTable',
    '#editProgramModal'
);
