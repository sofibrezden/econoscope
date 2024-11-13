import HomePage from "./pages/HomePage/HomePage";
import PredictorForm from "./pages/PredictorForm/PredictorForm"
import React from "react";
import { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Visualization from "./pages/HomePage/components/Visualization";
import Login from "./pages/HomePage/Login";
import UserHistoryPage from "./pages/UserHistoryPage/UserHistoryPage";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/predict" element={<PredictorForm />} />
        <Route path="/visualization" element={<Visualization />} />
        <Route path="/history" element={<UserHistoryPage />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
