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
