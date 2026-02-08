const balanceData = {
    balance: 7.68
};

document.getElementById("Live_Balance").innerText = "Balance - " + " ₹ " + balanceData.balance;

const buttonData = [
    {name: '₹ 10 Any Gift Card', value: 10, barClass: 'red-loading-bar'},
    {name: '₹ 100 Any Gift Card', value: 100, barClass: 'green-loading-bar'},
    {name: 'Free Fire 100 Diamonds', value: 80, barClass: 'blue-loading-bar'},
    {name: 'Free Fire 520 Diamonds', value: 400, barClass: 'yellow-loading-bar'},
    {name: 'BGMI 66 UC', value: 75, barClass: 'purple-loading-bar'},
    {name: 'GMI 80 UC', value: 100, barClass: 'orange-loading-bar'},
    {name: 'BGMI Royle Pass', value: 400, barClass: 'pink-loading-bar'}
];

let interval;

function updateBalance() {
    const balanceDisplay = document.getElementById('balance-display');
    balanceDisplay.textContent = `₹ ${balanceData.balance}`;
}

function buttonAction(index) {
    clearInterval(interval);
    
    const targetValue = buttonData[index].value;
    const popup = document.getElementById('popup');
    const loadingBar = document.getElementById('loading-bar');
    const buttonName = document.getElementById('popup-button-name');
    const displayBalance = document.getElementById('display-balance');
    const totalNeeded = document.getElementById('total-needed');
    const totalRemaining = document.getElementById('total-remaining');

    buttonName.textContent = buttonData[index].name;
    displayBalance.textContent = `Balance: ₹ ${balanceData.balance}`;
    totalNeeded.textContent = `Total Needed: ₹ ${targetValue}`;
    totalRemaining.textContent = `Total Remaining: ₹ ${targetValue - balanceData.balance}`;

    loadingBar.className = 'loading-bar ' + buttonData[index].barClass;
    
    popup.style.display = 'block';
    loadingBar.style.width = '0%';

    let percentage = 0;
    interval = setInterval(() => {
        if (percentage >= 100 || balanceData.balance >= targetValue) {
            clearInterval(interval);
            loadingBar.style.width = '100%';
        } else {
            percentage = (balanceData.balance / targetValue) * 100;
            loadingBar.style.width = `${percentage}%`;
        }
    }, 50);
}

function closePopup(event) {
    const popup = document.getElementById('popup');
    const closeBtn = document.querySelector('.close');
    
    if (event.target === popup || event.target === closeBtn) {
        popup.style.display = 'none';
        clearInterval(interval);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    updateBalance();
});
