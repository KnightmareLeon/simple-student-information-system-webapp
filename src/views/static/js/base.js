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

const sidebar = document.querySelector('.sidebar');
const toggleHeader = document.getElementById('sidebarToggle');

toggleHeader.addEventListener('click', () => {
    sidebar.classList.toggle('minimized');
    document.cookie = "sidebar=" + (sidebar.classList.contains('minimized') ? "minimized" : "expanded") + ";path=/";
});
