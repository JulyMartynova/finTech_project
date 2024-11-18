// script_w.js

const API_URL = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', () => {
    const createHotWalletButton = document.getElementById('create-hot-wallet');
    const createColdWalletButton = document.getElementById('create-cold-wallet');
    const cryptoSelect = document.getElementById('crypto-select');
    const walletsListDiv = document.getElementById('wallets-list');
    const resultDiv = document.getElementById('action-result');

    // Получение токена из sessionStorage
    const token = sessionStorage.getItem('access_token');

    if (!token) {
        alert('You must be logged in to view wallets.');
        window.location.href = 'login.html'; // Перенаправление на страницу логина
    }

    // Отображение кошельков пользователя
    async function fetchWallets() {
        const response = await fetch(`${API_URL}/wallet/all_wallets`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();
        if (response.ok && data.wallets) {
            walletsListDiv.innerHTML = data.wallets.map(wallet => `
                <div class="wallet">
                    <p><strong>Address:</strong> ${wallet.address}</p>
                    <p><strong>Type:</strong> ${wallet.is_cold ? 'Cold' : 'Hot'}</p>
                    <p><strong>Balance:</strong> ${wallet.balance} ${wallet.crypto}</p>
                    <button class="delete-wallet" data-address="${wallet.address}">Delete</button>
                </div>
            `).join('');

            // Добавить обработчик событий для кнопок удаления
            const deleteButtons = document.querySelectorAll('.delete-wallet');
            deleteButtons.forEach(button => {
                button.addEventListener('click', async (event) => {
                    const walletAddress = event.target.getAttribute('data-address');
                    await deleteWallet(walletAddress);
                });
            });
        } else {
            walletsListDiv.innerHTML = '<p>No wallets found.</p>';
        }
    }

    // Создание горячего кошелька
    createHotWalletButton.addEventListener('click', async () => {
        const crypto = cryptoSelect.value; // Получаем выбранную криптовалюту

        const response = await fetch(`${API_URL}/wallet/create/hot_wallet`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ crypto }) // Передаем данные в JSON формате
        });

        const data = await response.json();
        if (response.ok) {
            resultDiv.textContent = `Hot wallet created successfully! Address: ${data.address}`;
            fetchWallets(); // Перезагрузить список кошельков
        } else {
            resultDiv.textContent = `Error: ${data.message}`;
        }
    });

    // Создание холодного кошелька
    createColdWalletButton.addEventListener('click', async () => {
        const crypto = cryptoSelect.value; // Получаем выбранную криптовалюту

        const response = await fetch(`${API_URL}/wallet/create/cold_wallet`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ crypto }) // Передаем данные в JSON формате
        });

        const data = await response.json();
        if (response.ok) {
            resultDiv.textContent = `Cold wallet created successfully! Address: ${data.address}`;
            fetchWallets(); // Перезагрузить список кошельков
        } else {
            resultDiv.textContent = `Error: ${data.message}`;
        }
    });

    // Удаление кошелька
    async function deleteWallet(address) {
        const response = await fetch(`${API_URL}/wallet/remove`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ address }) // Передаем данные в JSON формате
        });

        const data = await response.json();
        if (response.ok) {
            resultDiv.textContent = `Wallet deleted successfully! Address: ${address}`;
            fetchWallets(); // Перезагрузить список кошельков
        } else {
            resultDiv.textContent = `Error: ${data.message}`;
        }
    }

    // Загружаем кошельки при загрузке страницы
    fetchWallets();
});
