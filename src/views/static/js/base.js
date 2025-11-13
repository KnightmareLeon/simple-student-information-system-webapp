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

$('#sidebarToggle').on('click', function() {
    const $sidebar = $('.sidebar');
    $sidebar.toggleClass('minimized');
    document.cookie = "sidebar=" + ($sidebar.hasClass('minimized') ? "minimized" : "expanded") + ";path=/";
});