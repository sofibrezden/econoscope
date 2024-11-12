import React, {useState, useEffect} from "react";
import axios from "axios";
import "./UnemploymentRatePredictor.scss";
import {Link} from "react-router-dom";

const UnemploymentRatePredictor = () => {
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("");
    const [country, setCountry] = useState("");
    const [year, setYear] = useState("");

    const [countries, setCountries] = useState([]);
    const [ages, setAges] = useState([]);
    const [genders, setGenders] = useState([]);

    const [prediction, setPrediction] = useState(null);

    useEffect(() => {
        // Отримати дані для форми з бекенду
        axios.get("http://localhost:5000/api/form-data")
            .then((response) => {
                console.log("Fetched form data:", response.data); // Вивід у консоль для перевірки отриманих даних
                setCountries(response.data.countries);
                setAges(response.data.ages);
                setGenders(response.data.sexes);
            })
            .catch((error) => {
                console.error("Error fetching form data:", error);
            });
    }, []);


    const handlePrediction = () => {
        axios.post("http://localhost:5000/predict", {
            country: country,
            age: age,
            sex: gender,
            year: year
        })
            .then((response) => {
                console.log("Prediction response:", response.data);
                setPrediction(response.data);
            })
            .catch((error) => {
                console.error("Error fetching prediction:", error);
            });
    };


    return (
        <div className="predictor-container">
            <h1>Unemployment Rate Predictor</h1>
            <div className="prediction-form">
                <h2>Forecasting Prediction Form</h2>

                <select value={age} onChange={(e) => setAge(e.target.value)}>
                    <option value="">Select Age</option>
                    {ages.map((ageOption, index) => (
                        <option key={index} value={ageOption}>
                            {ageOption}
                        </option>
                    ))}
                </select>

                <select value={gender} onChange={(e) => setGender(e.target.value)}>
                    <option value="">Select Gender</option>
                    {genders.map((genderOption, index) => (
                        <option key={index} value={genderOption}>
                            {genderOption}
                        </option>
                    ))}
                </select>

                <select value={country} onChange={(e) => setCountry(e.target.value)}>
                    <option value="">Select Country</option>
                    {countries.map((countryOption, index) => (
                        <option key={index} value={countryOption}>
                            {countryOption}
                        </option>
                    ))}
                </select>

                <input
                    type="number"
                    value={year}
                    onChange={(e) => setYear(e.target.value)}
                    placeholder="Select Year"
                />

                <button onClick={handlePrediction}>Predict</button>

                {prediction && (
                    <div className="prediction-result">
                        <p><strong>Forecasted Value:</strong> {prediction.prediction*100}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UnemploymentRatePredictor;
