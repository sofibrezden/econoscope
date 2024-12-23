import HomePage from "./pages/HomePage/HomePage";
import UnemploymentRatePredictorPage from "./pages/UnemploymentRatePredictorPage/UnemploymentRatePredictorPage";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Visualization from "./pages/Visualization/Visualization";
import Login from "./pages/Login/Login";
import UserHistoryPage from "./pages/UserHistoryPage/UserHistoryPage";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import RegisterPage from "./pages/RegistrationPage/Registration";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/predict" element={<UnemploymentRatePredictorPage />} />
        <Route path="/visualization" element={<Visualization />} />
        <Route path="/history" element={<UserHistoryPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
      <ToastContainer />
    </Router>
  );
}

export default App;
