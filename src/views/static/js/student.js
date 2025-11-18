//Handle Edit Button
$('#StudentTable').on('click', '.edit-btn', function () {
    const recordId = $(this).data('id');

    $.get(`/students/${recordId}`, function (resp) {
        if (resp.status === "success") {
            $('#editOriginalID').val(resp.data.id);
            $('#editID').val(resp.data.id);
            $('#editFirstName').val(resp.data.firstname);
            $('#editLastName').val(resp.data.lastname);
            $('input[name=editGender][value="' + resp.data.gender + '"]').prop('checked', true);
            $('input[name=editYearLevel][value="' + resp.data.yearlevel + '"]').prop('checked', true);
            $('#editYearLevel').val(resp.data.yearlevel);
            $('select[name=editForeignProgramCode]').selectpicker('val', resp.data.programcode);
            $('select[name=editForeignProgramCode]').selectpicker('render');
            $('#editStudentImage').attr('src', resp.data.image);
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
            $('#studentImg').attr('src', resp.data.image);
            $('#infoID').text(resp.data.id);
            $('#infoFirstName').text(resp.data.firstname);
            $('#infoLastName').text(resp.data.lastname);
            $('#infoGender').text(resp.data.gender);
            $('#infoYearLevel').text(resp.data.yearlevel);
            $('#infoForeignProgramCode').text(resp.data.programcode);
            $('#infoForeignProgramName').text(resp.data.programname);
            $('#infoStudentForeignCollegeCode').text(resp.data.collegecode);
            $('#infoStudentForeignCollegeName').text(resp.data.collegename);
            $('#infoStudentModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
});

//Handle Delete Avatar Button
$('#StudentTable').on('click', '.delete-avatar-btn', async function(){
    const recordId = $(this).data('id');

    const confirmed = await showConfirm('delete_avatar');

    if(!confirmed) return;

    $.ajax({
        url: `/students/avatar/${recordId}`,
        type: 'DELETE',
        success: function(resp) {
            if (resp.status === "success") {
                $('#StudentTable').DataTable().ajax.reload(null, false);
                showToast(resp.message, "success");
            } else {
                showToast(resp.message, "error");
            }
        },
        error: function(xhr, status, error) {
            showToast('An error occurred: ' + error, 'error');
        }
    });
})

$('#editStudentModal').on('show.bs.modal', function () {
    $('.pond').filepond('removeFiles');
});

$('#addStudentModal').on('show.bs.modal', function () {
    $('.pond').filepond('removeFiles');
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
        { data: "id" },
        { data: "firstname" },
        { data: "lastname" },
        { data: "gender" },
        { data: "yearlevel" },
        { data: "programcode" },
        { 
            data: "image",
            orderable: false,
            searchable: false,
            render: function(data){
                return `<div style="width: 64px">
                            <img src="${data}" alt="" class="img-fluid shadow rounded-circle">
                        </div>`;
            }
        },
        { data: "actions", orderable: false, searchable: false }
    ]
});

setupTableModal(
    '#addStudentForm',
    '#addStudentModal',
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

$.fn.filepond.registerPlugin(
    FilePondPluginImagePreview,
    FilePondPluginFileValidateSize
);

$('.pond').filepond({
    storeAsFile: true,
    maxFileSize: '5MB',
    labelMaxFileSizeExceeded: 'File is too large',
    labelMaxFileSize: 'Maximum file size is {filesize}'
});