// Mở modal khi nhấn vào nút "Thêm giao dịch"
const addTransactionBtn = document.getElementById('addTransactionBtn');
const addTransactionModal = document.getElementById('addTransactionModal');
const closeModalBtn = document.getElementById('closeModalBtn');

addTransactionBtn.addEventListener('click', () => {
    addTransactionModal.classList.remove('hidden');
});

// Đóng modal khi nhấn vào nút "Đóng"
closeModalBtn.addEventListener('click', () => {
    addTransactionModal.classList.add('hidden');
});