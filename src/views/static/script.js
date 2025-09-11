const sidebar = document.querySelector('.sidebar');
const toggleHeader = document.getElementById('sidebarToggle');

toggleHeader.addEventListener('click', () => {
    sidebar.classList.toggle('minimized');
    document.cookie = "sidebar=" + (sidebar.classList.contains('minimized') ? "minimized" : "expanded") + ";path=/";
});

let collegeTable = new DataTable('#CollegeTable');
let programTable = new DataTable('#ProgramTable');
let studentTable = new DataTable('#StudentTable');
