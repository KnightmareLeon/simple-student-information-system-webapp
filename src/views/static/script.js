const sidebar = document.querySelector('.sidebar');
const toggleHeader = document.getElementById('sidebarToggle');

toggleHeader.addEventListener('click', () => {
    sidebar.classList.toggle('minimized');
    document.cookie = "sidebar=" + (sidebar.classList.contains('minimized') ? "minimized" : "expanded") + ";path=/";
});

function setupTableModal(formSelector, modalSelector, alertSelector, tableSelector) {
    $(modalSelector).on('show.bs.modal', function () {
        $(alertSelector).addClass('d-none').removeClass('alert-success alert-danger').text('');
        $(formSelector)[0].reset();
        $(formSelector + ' input, ' + formSelector + ' select').removeClass('is-invalid');
    });

    $(formSelector).submit(function(e) {
        e.preventDefault();
        $.post($(this).attr('action'), $(this).serialize(), function(resp) {
            const $alert = $(alertSelector);
            if (resp.status === "success") {
                $alert.removeClass('d-none alert-danger').addClass('alert-success').text(resp.message);
                $(tableSelector).DataTable().ajax.reload(null, false);
                setTimeout(() => $(modalSelector).modal('hide'), 1000);
            } else {
                $alert.removeClass('d-none alert-success').addClass('alert-danger').text(resp.message);
            }
        });
    });
}

$('#recordProgramPrimaryCode, #recordProgramName').on('blur input', function() {
    let code = $('#recordProgramPrimaryCode').val().trim();
    let name = $('#recordProgramName').val().trim();
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

$('#recordCollegePrimaryCode, #recordCollegeName').on('blur input', function() {
    let code = $('#recordCollegePrimaryCode').val().trim();
    let name = $('#recordCollegeName').val().trim();
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
    ],
    rowCallback: function(row, data) {
    if (!$('#editRecordModal' + data.id).length) {
        $('body').append(data.modal);
    }
}
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
    ],
    rowCallback: function(row, data) {
    if (!$('#editRecordModal' + data.id).length) {
        $('body').append(data.modal);
    }
}
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
    ],
    rowCallback: function(row, data) {
    if (!$('#editRecordModal' + data.id).length) {
        $('body').append(data.modal);
    }
}
});

setupTableModal('#addCollegeForm', '#addCollegeModal', '#addCollegeFormAlert', '#CollegeTable');
setupTableModal('#addProgramForm', '#addProgramModal', '#addProgramFormAlert', '#ProgramTable');
setupTableModal('#addStudentForm', '#addStudentModal', '#addStudentFormAlert', '#StudentTable');

$('#ProgramTable').on('click', '.edit-btn', function () {
    let id = $(this).data('id');
    $.ajax({
        url: `/programs/${id}/edit-form`,
        type: 'GET',
        success: function (html) {
            $('#editRecordModal .modal-content').html(`
                <div class="modal-header">
                    <h5 class="modal-title">Edit Program</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">${html}</div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" form="editRecordForm" class="btn btn-primary">Save</button>
                </div>
            `);
            $('#editRecordModal').modal('show');
        }
    });
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

