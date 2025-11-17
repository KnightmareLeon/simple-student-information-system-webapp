//Handle Edit Button
$('#ProgramTable').on('click', '.edit-btn', function () {
    const recordId = $(this).data('id');

    $.get(`/programs/${recordId}`, function (resp) {
        if (resp.status === "success") {
            $('#editOriginalProgramCode').val(resp.data.code);
            $('#editProgramPrimaryCode').val(resp.data.code);
            $('#editProgramName').val(resp.data.name);
            $('select[name=editForeignCollegeCode]').selectpicker('val', resp.data.collegecode);
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
            $('#infoProgramName').text(resp.data.name);
            $('#infoForeignCollegeCode').text(resp.data.collegecode);
            $('#infoForeignCollegeName').text(resp.data.collegename);
            $('#infoProgramStudentCount').text(resp.data.totalstds);
            $('#infoProgramModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
    
});

let programTable = $('#ProgramTable').DataTable({
    processing: true, 
    serverSide: true,
    scrollX: true,
    ajax: {
        url: "/programs/data",
        type: "POST"
    },
    columns: [
        { data: "code" },
        { data: "name" },
        { data: "collegecode" },
        { data: "actions", orderable: false, searchable: false }
    ]
});

setupTableModal(
    '#addProgramForm',
    '#addProgramModal',
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
