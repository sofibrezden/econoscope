import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "../components/RegisterForm.scss";
import styles from "./RegisterForm.module.scss";
import { Field, Form, Formik } from "formik";
import SignUp from "../../../assets/sign_up.png";
import { toast } from "react-toastify";

const Register = () => {
  const navigate = useNavigate();

  const handleRegister = async (value) => {
    if (!value.username || !value.email || !value.password) {
      toast.error("Fields are required ");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:5000/register",
        value,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      navigate("/login");
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        toast.error(err.response.data.error);
      } else {
        toast.error("An error occurred during registration");
      }
    }
  };

  return (
    <>
      <div className={styles.root}>
        <div>
          <h1>Econoscope</h1>
          <Formik
            initialValues={{
              email: "",
              username: "",
              password: "",
            }}
            onSubmit={handleRegister}
          >
            <Form className={styles.form}>
              <p className={styles.welcome_back}>Join us now</p>
              <div>
                <label htmlFor="username">Username </label>
                <Field id="username" name="username" placeholder="username" />
              </div>
              <div>
                <label htmlFor="username">Email </label>
                <Field
                  id="email"
                  name="email"
                  placeholder="yourmail@gmail.com"
                />
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
              </div>
            </Form>
          </Formik>
        </div>
        <div className={styles.container_for_image}>
          <img src={SignUp} alt="Auth Image" fill />
        </div>
      </div>
    </>
  );
};

export default Register;
