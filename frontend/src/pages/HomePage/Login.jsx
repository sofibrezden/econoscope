import React from "react";
import "./Login.css";
import Header from "./components/Header/Header";
import styles from "./Login.module.scss";
import {Field, Form, Formik} from "formik";
import LogIn from "../../assets/login.png";

function Login() {
    const handleSubmit = async (value) => {
        try {
            const response = await fetch("http://localhost:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(value),
            });

            console.log("Response status:", response.status);
            console.log("Response headers:", response.headers);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Login failed: ${errorText}`);
            }

            const contentType = response.headers.get('Content-Type');
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                const {token} = data;
                localStorage.setItem('authToken', token);
                window.location.href = "/";
            } else {
                throw new Error("Unexpected response format: not JSON");
            }
        } catch (error) {
            console.error("Login failed:", error.message);
            alert(error.message);
        }
    };


    return (
        <>
            <Header/>
            <div className={styles.root}>
                <div>
                    <h1>Econoscope</h1>
                    <Formik
                        initialValues={{
                            username: "",
                            password: "",
                        }}
                        onSubmit={handleSubmit}
                    >
                        <Form className={styles.form}>
                            <p className={styles.welcome_back}>Welcome Back</p>
                            <div>
                                <label htmlFor="username">Username </label>
                                <Field id="username" name="username" placeholder="Username"/>
                            </div>
                            <div>
                                <label htmlFor="password">Password </label>
                                <Field
                                    id="password"
                                    name="password"
                                    type="password"
                                    placeholder="∗∗∗∗∗∗∗∗∗∗∗"
                                />
                            </div>
                            <div className={styles.buttons_container}>
                                <button className={styles.sign_up_button}>Login</button>
                                <p className={styles.sub_text}>
                                    Don`t have an account?{" "}
                                    <a href="/register" className={styles.sign_in_link}>
                                        <b>Sign Up</b>
                                    </a>{" "}
                                </p>
                            </div>
                        </Form>
                    </Formik>
                </div>
                <div className={styles.container_for_image}>
                    <img src={LogIn} alt="Auth Image" fill/>
                </div>
            </div>
        </>
    );
}

export default Login;
