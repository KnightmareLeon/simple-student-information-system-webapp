//Handle Edit Button
$('#CollegeTable').on('click', '.edit-btn', function () {
    const recordId = $(this).data('id');

    $.get(`/colleges/${recordId}`, function (resp) {
        if (resp.status === "success") {
            $('#editOriginalCollegeCode').val(resp.data.code);
            $('#editCollegePrimaryCode').val(resp.data.code);
            $('#editCollegeName').val(resp.data.name);
            $('#editCollegeModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
});

//Handle Info Button
$('#CollegeTable').on('click', '.info-btn', function () {
    const collegeCode = $(this).data('id')
    $.get(`/colleges/info/${collegeCode}`, function(resp){
        if (resp.status === "success") {
            $('#infoCollegeCode').text(collegeCode);
            $('#infoCollegeName').text(resp.data.name);
            $('#infoCollegeTotalPrograms').text(resp.data.totalprgs);
            $('#infoCollegeTotalStudents').text(resp.data.totalstds);
            $('#infoCollegeModal').modal('show');
        } else {
            showToast(resp.message, "error");
        }
    });
});

let collegeTable = $('#CollegeTable').DataTable({
    processing: true, 
    serverSide: true,
    scrollX: true,
    ajax: {
        url: "/colleges/data",
        type: "POST"
    },
    columns: [
        { data: "code" },
        { data: "name" },
        { data: "actions", orderable: false, searchable: false }
    ]
});

setupTableModal(
    '#addCollegeForm',
    '#addCollegeModal',
    '#addCollegeFormAlert',
    '#CollegeTable',
    'None'
);

setupDeleteHandler(
    '#CollegeTable',
    'colleges'
);

setupEditSubmit(
    '#editCollegeForm',
    '#CollegeTable',
    '#editCollegeModal'
);