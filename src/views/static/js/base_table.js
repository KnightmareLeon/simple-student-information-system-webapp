function showConfirm(action) {
    return new Promise((resolve) => {
        const $modal = $('#confirmationModal');
        const $confirmBtn = $('#confirmBtn');
        const $confirmTitle = $('#confirmTitle');
        const $confirmDialog = $('#confirmDialog');
        const modal = new bootstrap.Modal($modal[0]);

        const config = {
            delete: {
                btnClass: 'btn-danger',
                title: 'Confirm Delete Action',
                text: 'Please confirm that you want to delete this record.'
            },
            edit: {
                btnClass: 'btn-primary',
                title: 'Confirm Update Action',
                text: 'Please confirm that you want to update this record.'
            },
            add: {
                btnClass: 'btn-primary',
                title: 'Confirm Add Action',
                text: 'Please confirm that you want to add this record.'
            }
        };

        const { btnClass, title, text } = config[action] || config.add;

        $confirmBtn.removeClass('btn-primary btn-danger').addClass(btnClass);
        $confirmTitle.text(title);
        $confirmDialog.text(text);

        const cleanup = () => {
            $confirmBtn.off('click', onConfirm);
            $modal.off('hide.bs.modal', onHide);
        };

        const onConfirm = () => {
            cleanup();
            modal.hide();
            resolve(true);
        };

        const onHide = () => {
            cleanup();
            resolve(false);
        };

        $confirmBtn.on('click', onConfirm);
        $modal.on('hide.bs.modal', onHide);

        modal.show();
    });
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

    $(formSelector).submit(async function(e) {
        e.preventDefault();
        const confirmed = await showConfirm('add');
        if (!confirmed) return;

        const formData = new FormData(this);

        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(resp) {
                if (resp.status === "success") {
                    $(tableSelector).DataTable().ajax.reload(null, false);
                    $(modalSelector).modal('hide');
                    showToast(resp.message, "success");
                } else {
                    showToast(resp.message, "error");
                }
            },
            error: function(err) {
                showToast("An error occurred while sending data", "error");
            }
        });
    });
}


function setupDeleteHandler(tableSelector, entity) {
    $(tableSelector).on('click', '.delete-btn', async function () {
        const recordId = $(this).data('id');

        const confirmed = await showConfirm('delete');
        if (!confirmed) return;

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
    $(formSelector).submit(async function(e) {
        e.preventDefault();

        const confirmed = await showConfirm('edit');
        if (!confirmed) return;

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