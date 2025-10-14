//Check Duplicates
$('#addID').on('blur input', function() {
    let id = $('#addID').val().trim();
    if (!id) return;

    $.get('/students/check_duplicates', { id : id }, function(resp) {
        const $alert = $('#addStudentFormAlert');
        if (resp.exists) {
            $alert.removeClass('d-none alert-success').addClass('alert-danger').text(`ID number ${id} already exists.`);
        } else {
            $alert.addClass('d-none');
        }
    });
});

//Handle Edit Button
$('#StudentTable').on('click', '.edit-btn', function () {
    const recordId = $(this).data('id');

    $.get(`/students/get_edit_info/${recordId}`, function (resp) {
        if (resp.status === "success") {
            $('#editOriginalID').val(resp.data.ID);
            $('#editID').val(resp.data.ID);
            $('#editFirstName').val(resp.data.FirstName);
            $('#editLastName').val(resp.data.LastName);
            $('input[name=editGender][value="' + resp.data.Gender + '"]').prop('checked', true);
            $('input[name=editYearLevel][value="' + resp.data.YearLevel + '"]').prop('checked', true);
            $('#editYearLevel').val(resp.data.YearLevel);
            $('select[name=editForeignProgramCode]').selectpicker('val', resp.data.ProgramCode);
            $('select[name=editForeignProgramCode]').selectpicker('render');
            $('#editStudentModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
});

//Handle Info Button
$('#StudentTable').on('click', '.info-btn', function () {
    const studentID = $(this).data('id')
    $.get(`/students/info/${studentID}`, function(resp){
        if (resp.status === "success") {
            $('#infoID').text(resp.data.ID);
            $('#infoFirstName').text(resp.data.FirstName);
            $('#infoLastName').text(resp.data.LastName);
            $('#infoGender').text(resp.data.Gender);
            $('#infoYearLevel').text(resp.data.YearLevel);
            $('#infoForeignProgramCode').text(resp.data.ProgramCode);
            $('#infoForeignProgramName').text(resp.data.ProgramName);
            $('#infoStudentForeignCollegeCode').text(resp.data.CollegeCode);
            $('#infoStudentForeignCollegeName').text(resp.data.CollegeName);
            $('#infoStudentModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
    
});

let studentTable = $('#StudentTable').DataTable({
    processing: true, 
    serverSide: true,
    scrollX: true,
    ajax: {
        url: "/students/data",
        type: "POST"
    },
    columns: [
        { data: "ID" },
        { data: "FirstName" },
        { data: "LastName" },
        { data: "Gender" },
        { data: "YearLevel" },
        { data: "ProgramCode" },
        { data: "actions", orderable: false, searchable: false }
    ]
});

setupTableModal(
    '#addStudentForm',
    '#addStudentModal',
    '#addStudentFormAlert',
    '#StudentTable',
    'addForeignProgramCode'
);

setupDeleteHandler(
    '#StudentTable',
    'students'
);

setupEditSubmit(
    '#editStudentForm',
    '#StudentTable',
    '#editStudentModal'
);
