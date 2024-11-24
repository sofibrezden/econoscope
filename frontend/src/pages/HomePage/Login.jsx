import React from "react";
import "./Login.css";
import Header from "./components/Header/Header";
import styles from "./Login.module.scss";
import { Field, Form, Formik } from "formik";
import LogIn from "../../assets/login.png";

function Login() {
  const handleSubmit = async (value) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(value),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Login failed");
      }

      const { token } = await response.json();
      localStorage.setItem("authToken", token);

      // Запит із токеном для перевірки автентифікації
      const authCheck = await fetch("http://127.0.0.1:5000/check-auth", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`, // Додавання токена в заголовок
        },
      });

      if (!authCheck.ok) {
        const errorData = await authCheck.json();
        throw new Error(errorData.error || "Authentication check failed");
      }

      const authStatus = await authCheck.json();

      if (authStatus.authenticated) {
        console.log("User authenticated");
        window.location.href = "/";
      } else {
        console.error("Authentication check failed.");
      }
    } catch (error) {
      console.error("Login failed:", error.message);
      alert(error.message);
    }
  };

  return (
    <>
      <Header />
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
                <Field id="username" name="username" placeholder="Oleg" />
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
                <button className={styles.sign_up_button}>Sign Up</button>
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
          <img src={LogIn} alt="Auth Image" fill />
        </div>
      </div>
    </>
  );
}

export default Login;
