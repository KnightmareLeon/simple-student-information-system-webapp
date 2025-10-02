function showToast(message, type = "success", position = "top-0 start-50 translate-middle-x") {
    const $toast = $('#mainToast');
    const $container = $('#toastContainer');

    $container.removeClass().addClass(`position-fixed ${position} p-3`).css('z-index', 1100);

    $toast.removeClass("text-bg-success text-bg-danger text-bg-warning");
    if (type === "success") $toast.addClass("text-bg-success");
    if (type === "error") $toast.addClass("text-bg-danger");
    if (type === "warning") $toast.addClass("text-bg-warning");

    $('#toastBody').text(message);

    const toast = new bootstrap.Toast($toast[0]);
    toast.show();
}

function setupTableModal(formSelector, modalSelector, alertSelector, tableSelector, selectpickerSelector) {
    $(modalSelector).on('show.bs.modal', function () {
        $(alertSelector).addClass('d-none').removeClass('alert-success alert-danger').text('');
        $(formSelector)[0].reset();
        $(formSelector + ' input, ' + formSelector + ' select').removeClass('is-invalid');
        if (selectpickerSelector !== 'None') {
            $(`select[name=${selectpickerSelector}]`).selectpicker('destroy');
            $(`select[name=${selectpickerSelector}]`).selectpicker();
        }
    });

    $(formSelector).submit(function(e) {
        e.preventDefault();
        $.post($(this).attr('action'), $(this).serialize(), function(resp) {
            if (resp.status === "success") {
                $(tableSelector).DataTable().ajax.reload(null, false);
                $(modalSelector).modal('hide');
                showToast(resp.message, "success");
            } else {
                showToast(resp.message, "error");
            }
        });
    });
}

function setupDeleteHandler(tableSelector, entity) {
    $(tableSelector).on('click', '.delete-btn', function () {
        const recordId = $(this).data('id');

        if (!confirm("Are you sure you want to delete this record?")) return;

        $.post(`/${entity}/delete/${recordId}`, function (resp) {
            if (resp.status === "success") {
                $(tableSelector).DataTable().ajax.reload(null, false);
                showToast(resp.message, "success");
            } else {
                showToast(resp.message, "error");
            }
        });
    });
}

function setupEditSubmit(formSelector, tableSelector, modalSelector) {

    $(formSelector).submit(function(e) {
        e.preventDefault();

        $.post($(this).attr('action'), $(this).serialize(), function (resp) {
            if (resp.status === "success") {
                $(tableSelector).DataTable().ajax.reload(null, false);
                $(modalSelector).modal('hide');
                showToast(resp.message, "success");
            } else {
                showToast(resp.message, "error");
            }
        });
    });
}

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

$('#addCollegePrimaryCode, #addCollegeName').on('blur input', function() {
    let code = $('#addCollegePrimaryCode').val().trim();
    let name = $('#addCollegeName').val().trim();
    if (!code && !name) return;

    $.get('/colleges/check_duplicates', { code: code, name: name }, function(resp) {
        const $alert = $('#addCollegeFormAlert');
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

$('#CollegeTable').on('click', '.edit-btn', function () {
    const recordId = $(this).data('id');

    $.get(`/colleges/get_edit_info/${recordId}`, function (resp) {
        if (resp.status === "success") {
            $('#editOriginalCollegeCode').val(resp.data.Code);
            $('#editCollegePrimaryCode').val(resp.data.Code);
            $('#editCollegeName').val(resp.data.Name);

            $('#editCollegeModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
});

$('#CollegeTable').on('click', '.info-btn', function () {
    const collegeCode = $(this).data('id')
    $.get(`/colleges/info/${collegeCode}`, function(resp){
        if (resp.status === "success") {
            $('#infoCollegeCode').text(collegeCode);
            $('#infoCollegeName').text(resp.data.Name);
            $('#infoCollegeTotalPrograms').text(resp.data.TotalPrograms);
            $('#infoCollegeTotalStudents').text(resp.data.TotalStudents);
            $('#infoCollegeModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
});

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

const sidebar = document.querySelector('.sidebar');
const toggleHeader = document.getElementById('sidebarToggle');

toggleHeader.addEventListener('click', () => {
    sidebar.classList.toggle('minimized');
    document.cookie = "sidebar=" + (sidebar.classList.contains('minimized') ? "minimized" : "expanded") + ";path=/";
});

DataTable.type('num', 'className', '');

let collegeTable = $('#CollegeTable').DataTable({
    processing: true, 
    serverSide: true, 
    ajax: {
        url: "/colleges/data",
        type: "POST"
    },
    columns: [
        { data: "Code" },
        { data: "Name" },
        { data: "actions", orderable: false, searchable: false }
    ]
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

let studentTable = $('#StudentTable').DataTable({
    processing: true, 
    serverSide: true, 
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

setupTableModal('#addCollegeForm', '#addCollegeModal', '#addCollegeFormAlert', '#CollegeTable', 'None');
setupTableModal('#addProgramForm', '#addProgramModal', '#addProgramFormAlert', '#ProgramTable', 'addForeignCollegeCode');
setupTableModal('#addStudentForm', '#addStudentModal', '#addStudentFormAlert', '#StudentTable', 'addForeignProgramCode');

setupDeleteHandler('#CollegeTable','colleges');
setupDeleteHandler('#ProgramTable','programs');
setupDeleteHandler('#StudentTable','students');

setupEditSubmit('#editCollegeForm', '#CollegeTable', '#editCollegeModal');
setupEditSubmit('#editProgramForm', '#ProgramTable', '#editProgramModal');
setupEditSubmit('#editStudentForm', '#StudentTable', '#editStudentModal');

$('.uppercase-field').on('input', function(){
    $(this).val($(this).val().toUpperCase());
});

const ctx = document.getElementById('dashboardStudentChart').getContext('2d');
const myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
    labels: ['2022', '2023', '2024', '2025'],
    datasets: [{
        label: 'Male',
        data: [10, 50, 30, 50],
        backgroundColor: 'rgba(54, 162, 235, 0.7)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
    },
    {
        label: 'Female',
        data: [10, 50, 30, 50],
        backgroundColor: 'rgba(235, 54, 54, 0.7)',
        borderColor: 'rgba(235, 54, 54, 1)',
        borderWidth: 1
    },
    {
        label: 'LQGBTQIA+',
        data: [10, 50, 30, 50],
        backgroundColor: 'rgba(235, 214, 54, 0.7)',
        borderColor: 'rgba(235, 229, 54, 1)',
        borderWidth: 1
    }]
    },
    options: {
    responsive: true,
    maintainAspectRatio: false,
        scales: {
        y: { beginAtZero: true }
        }
    }
});