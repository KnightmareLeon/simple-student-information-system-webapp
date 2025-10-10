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

        if (!confirm("Are you sure you want to update this record?")) return;

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

$.ajaxSetup({
    headers: { "X-CSRFToken": $('meta[name="csrf-token"]').attr('content') }
});

DataTable.type('num', 'className', '');

$('.uppercase-field').on('input', function(){
    $(this).val($(this).val().toUpperCase());
});