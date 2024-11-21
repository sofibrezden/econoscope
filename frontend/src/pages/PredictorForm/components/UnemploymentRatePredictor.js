import React, {useState, useEffect} from "react";
import axios from "axios";
import "./UnemploymentRatePredictor.scss";
import {Link} from "react-router-dom";
import Header from "../../HomePage/components/Header/Header";

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
        console.log("Fetching form data from backend..."); // Лог для перевірки початку запиту
        axios.get("http://localhost:5000/form-data")
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

    const handlePreparePrediction = () => {
        console.log("Preparing prediction..."); // Лог для початку підготовки прогнозу

        axios.post("http://localhost:5000/prepare-predict", {
            country: country,
            age: age,
            sex: gender,
            year: year
        })
            .then((response) => {
                console.log("Prediction response:", response.data); // Лог результату прогнозу
                setPrediction(response.data);
                handleSavePrediction(response.data); // Зберегти прогноз після отримання відповіді
            })
            .catch((error) => {
                console.error("Error fetching prediction:", error);
            });
    };

    const handleSavePrediction = (predictionData) => {
        console.log("Saving prediction..."); // Лог для початку збереження прогнозу
        const token = localStorage.getItem("authToken"); // Отримання токена із localStorage
        if (!token) {
            console.log("User is not logged in. Prediction will not be saved."); // Лог, якщо токен відсутній
            return;
        }

        console.log("Token found, sending save request..."); // Лог токена перед запитом
        axios.post("http://localhost:5000/save-prediction", {
            model: predictionData.model,
            r_squared: predictionData.r_squared,
            rmse: predictionData.rmse,
            prediction: predictionData.prediction,
            country: predictionData.country,
            age: predictionData.age,
            sex: predictionData.sex,
            year: predictionData.year
        }, {
            headers: {
                'Authorization': `Bearer ${token}`, // Додати токен у заголовок
            }
        })
            .then((response) => {
                console.log("Save prediction response:", response.data); // Лог результату збереження
            })
            .catch((error) => {
                console.error("Error saving prediction:", error);
            });
    };

    return (
        <><Header/>


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

                    <button onClick={handlePreparePrediction}>Predict</button>

                    {prediction && (
                        <div className="prediction-result">
                            <p><strong>Forecasted Value:</strong> {prediction.prediction * 100}</p>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
};

export default UnemploymentRatePredictor;