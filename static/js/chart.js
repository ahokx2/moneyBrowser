const ctx = document.getElementById('financialChart').getContext('2d');
const canvas = document.getElementById('financialChart');
// canvas.width = 400;  // Kích thước chiều rộng
// canvas.height = 400; // Kích thước chiều cao

new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Thu nhập', 'Chi tiêu'],
        datasets: [{
            data: [5000000, 3000000],
            backgroundColor: ['#3b82f6', '#ef4444'],
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
