// URL вашего API
const API_URL = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', () => {

    // Обработчик для формы регистрации
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('register-username').value;
            const password = document.getElementById('register-password').value;

            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            const resultDiv = document.getElementById('register-result');

            if (response.ok) {
                resultDiv.textContent = 'User registered successfully!';
            } else {
                resultDiv.textContent = `Error: ${data.message}`;
            }
        });
    }

    // Обработчик для формы логина
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('login-username').value;
            const password = document.getElementById('login-password').value;

            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            const resultDiv = document.getElementById('login-result');

            if (response.ok) {
                // Сохраняем токен в sessionStorage
                sessionStorage.setItem('access_token', data.access_token);
                resultDiv.textContent = 'Login successful! Redirecting to trading...';
                window.location.href = 'trade.html'; // Перенаправляем на страницу торговли
            } else {
                resultDiv.textContent = `Error: ${data.message}`;
            }
        });
    }
});
