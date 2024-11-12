import HomePage from "./pages/HomePage/HomePage";
import PredictorForm from "./pages/PredictorForm/PredictorForm"
import React from "react";
import { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/predict" element={<PredictorForm />} />
      </Routes>
    </Router>
  );
}

export default App;