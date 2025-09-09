const sidebar = document.querySelector('.sidebar');
const toggleHeader = document.getElementById('sidebarToggle');

toggleHeader.addEventListener('click', () => {
    sidebar.classList.toggle('minimized');
    document.cookie = "sidebar=" + (sidebar.classList.contains('minimized') ? "minimized" : "expanded") + ";path=/";
});

$('#filter').editableSelect({
	effects: 'slide',
	duration: 200,
    filter: false
});

$('#recordCollegeCode').editableSelect({
	effects: 'slide',
	duration: 200,
});

$('#recordProgramCode').editableSelect({
	effects: 'slide',
	duration: 200,
});