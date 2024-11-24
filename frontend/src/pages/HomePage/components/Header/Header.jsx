import React, {useState, useEffect} from "react";
import {Link, useNavigate} from "react-router-dom";
import styles from "./Header.module.scss";
import EconoscopeLogo from "../../../../assets/econoscope_logo.png";
import EconoscopeTitle from "../../../../assets/econoscope_title.png";

function Header() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    // Check if the user is authenticated via JWT
    useEffect(() => {
        const checkAuthStatus = async () => {
            try {
                const token = localStorage.getItem("authToken"); // Get token from localStorage
                if (!token) {
                    setIsAuthenticated(false);
                    return;
                }

                const response = await fetch("http://127.0.0.1:5000/check-auth", {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    setIsAuthenticated(true);
                } else {
                    setIsAuthenticated(false);
                }
            } catch (error) {
                console.error("Failed to check authentication status:", error);
                setIsAuthenticated(false);
            }
        };

        checkAuthStatus();
    }, []); // Runs only on mount

    // Logout handler
    const handleLogout = async () => {
        try {
            const token = localStorage.getItem("authToken"); // Get token from localStorage
            if (!token) {
                console.error("No token found for logout");
                return;
            }

            const response = await fetch("http://127.0.0.1:5000/logout", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Logout failed");
            }

            console.log("Logout successful");
            localStorage.removeItem("authToken"); // Remove token from localStorage
            setIsAuthenticated(false); // Update auth state
            navigate("/"); // Redirect to login page after logout
        } catch (error) {
            console.error("Logout error:", error.message);
        }
    };

    return (
        <div className={styles.headerContainer}>
            <Link to="/">
                <div className={styles.logoContainer}>
                    <img src={EconoscopeLogo} className={styles.logo} alt="Econoscope Logo"/>
                    <img src={EconoscopeTitle} className={styles.title} alt="Econoscope Title"/>
                </div>
            </Link>
            <div className={styles.buttonsContainer}>
                <Link to="/predict">Predict</Link>
                <Link to="/visualization">Visualization</Link>

                {isAuthenticated ? (
                    <>
                        <Link to="/history">History</Link>
                        <button className={styles.logOutButton} onClick={handleLogout}>Log out</button>
                    </>
                ) : (
                    <>
                        <Link to="/login">
                            <button className={styles.signInButton}>Sign in</button>
                        </Link>
                        <Link to="/register">
                            <button className={styles.signUpButton}>Sign up</button>
                        </Link>
                    </>
                )}
            </div>
        </div>
    );
}

export default Header;
