import React, {useState} from 'react';
import './Login.css';
import Header from "./components/Header/Header";

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({username, password}),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Login failed');
            }

            const {token} = await response.json();
            localStorage.setItem('authToken', token);

            // Запит із токеном для перевірки автентифікації
            const authCheck = await fetch('http://127.0.0.1:5000/check-auth', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`, // Додавання токена в заголовок
                },
            });

            if (!authCheck.ok) {
                const errorData = await authCheck.json();
                throw new Error(errorData.error || 'Authentication check failed');
            }

            const authStatus = await authCheck.json();

            if (authStatus.authenticated) {
                console.log("User authenticated");
                window.location.href = '/';
            } else {
                console.error('Authentication check failed.');
            }
        } catch (error) {
            console.error('Login failed:', error.message);
            alert(error.message);
        }
    };

    return (
        <>
            <Header/>

            <div className="wrapper">
                <form id="loginForm" onSubmit={handleSubmit}>
                    <h1>Login</h1>
                    <div className="input-box">
                        <input
                            type="text"
                            id="username"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                        <i className="bx bx-envelope"></i>
                    </div>

                    <div className="input-box">
                        <input
                            type="password"
                            id="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <i className="bx bxs-lock-alt"></i>
                    </div>
                    <button className="login" type="submit">Sign In</button>
                </form>

                <div className="register-link">
                    <p>Don't have an account? <a href="/register">Register</a></p>
                </div>
            </div>
        </>
    );
}

export default Login;
