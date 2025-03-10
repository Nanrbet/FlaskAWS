// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initial load
    updateBalances();
});

async function updateBalances() {
    try {
        const response = await fetch('/api/balances');
        const data = await response.json();

        // Update balance values dynamically
        data.balances.forEach(balance => {
            const currency = balance.currency;
            const balanceValue = balance.balance;

            // Find the corresponding balance card and update the balance value
            const balanceCard = document.querySelector(`.balance-item:has(.label:contains("${currency}"))`);
            if (balanceCard) {
                const balanceValueElement = balanceCard.querySelector('.balance-value');
                if (balanceValueElement) {
                    balanceValueElement.textContent = balanceValue;
                    balanceValueElement.style.opacity = 0;
                    setTimeout(() => {
                        balanceValueElement.style.opacity = 1;
                        balanceValueElement.style.transition = 'opacity 0.5s';
                    }, 100);
                }
            }
        });
        
    } catch (error) {
        console.error('Error fetching balances:', error);
    }
}
