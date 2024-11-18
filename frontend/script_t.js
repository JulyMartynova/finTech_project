document.addEventListener("DOMContentLoaded", () => {
    // Функция для загрузки кошельков
    function loadWallets() {
        fetch("http://localhost:5000/wallet/all_wallets", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${sessionStorage.getItem("access_token")}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.wallets) {
                const walletSelect = document.getElementById("wallet");
                data.wallets.forEach(wallet => {
                    const option = document.createElement("option");
                    option.value = wallet.address;
                    option.textContent = `${wallet.is_cold ? "Cold" : "Hot"} Wallet - ${wallet.address}`;
                    walletSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error("Error loading wallets:", error);
        });
    }

    // Загрузить кошельки при загрузке страницы
    loadWallets();

    // Обработчик формы
    const tradeForm = document.getElementById("trade-form");
    tradeForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const transactionType = document.getElementById("transaction-type").value;
        const walletAddress = document.getElementById("wallet").value;
        const crypto = document.getElementById("crypto").value;
        const amount = document.getElementById("amount").value;

        const tradeData = {
            type: transactionType,
            wallet: walletAddress,
            crypto: crypto,
            amount: amount
        };

        fetch("http://localhost:5000/trade", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${sessionStorage.getItem("access_token")}`
            },
            body: JSON.stringify(tradeData)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("trade-result").textContent = `Order placed successfully: ${data.message}`;
        })
        .catch(error => {
            console.error("Error placing order:", error);
            document.getElementById("trade-result").textContent = "Error placing order.";
        });
    });
});
