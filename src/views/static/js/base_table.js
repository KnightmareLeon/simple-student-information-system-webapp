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
        if (!confirm("Are you sure you want to add this record?")) return;

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

        $.ajax({
            url: `/${entity}/${recordId}`,
            type: 'DELETE',
            success: function(resp) {
                if (resp.status === "success") {
                    $(tableSelector).DataTable().ajax.reload(null, false);
                    showToast(resp.message, "success");
                } else {
                    showToast(resp.message, "error");
                }
            },
            error: function(xhr, status, error) {
                showToast('An error occurred: ' + error, 'error');
            }
        });
    });
}

function setupEditSubmit(formSelector, tableSelector, modalSelector, entity) {
    $(formSelector).submit(function(e) {
        e.preventDefault();

        if (!confirm("Are you sure you want to update this record?")) return;

        $.ajax({
            url: `/${entity}`,
            type: 'PUT',
            data: $(this).serialize(),
            success: function(resp) {
                if (resp.status === "success") {
                    $(tableSelector).DataTable().ajax.reload(null, false);
                    $(modalSelector).modal('hide');
                    showToast(resp.message, "success");
                } else {
                    showToast(resp.message, "error");
                }
            },
            error: function(xhr, status, error) {
                showToast('An error occurred: ' + error, 'error');
            }
        });
    });
}

$.ajaxSetup({
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') }
});

DataTable.type('num', 'className', '');

$('.uppercase-field').on('input', function(){
    $(this).val($(this).val().toUpperCase());
});