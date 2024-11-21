import { Field, Form, Formik } from "formik";
import styles from "./UnemploymentRatePredictorSection.module.scss";
import { useCallback, useEffect, useState } from "react";
import axios from "axios";
import ChartImage from "../../../assets/chart.png";
import { toast } from "react-toastify";

function UnemploymentRatePredictorSection() {
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [country, setCountry] = useState("");
  const [year, setYear] = useState("");

  const [countries, setCountries] = useState([]);
  const [ages, setAges] = useState([]);
  const [genders, setGenders] = useState([]);

  const [result, setResult] = useState("");

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

  const handlePrediction = useCallback(async (values) => {
    try {
      const data = await axios.post("http://localhost:5000/prepare-predict", values);
      const predictionValue = data.data.prediction * 100; // Extract and scale the prediction
      setResult(predictionValue.toFixed(2));
      handleSavePrediction(data.data);
    } catch (error) {
      setResult("");
      toast.error("Wrong Data");
    }
  }, []);

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
    <div className={styles.container}>
      <h1 className={styles.sectionTitle}>Unemployment Rate Predictor</h1>
      <div>
        <div className={styles.formContainer}>
          <h3 className={styles.formTitle}>Forecasting Prediction Form</h3>
          <Formik
            initialValues={{ age: "", sex: "", country: "", year: "" }}
            onSubmit={handlePrediction}
          >
            <Form className={styles.inputContainer}>
              <div>
                <Field as="select" name="age">
                  <option disabled value="">
                    Select Age
                  </option>
                  {ages.map((item) => (
                    <option value={item} key={item}>
                      {item}
                    </option>
                  ))}
                </Field>
              </div>

              <div>
                <Field as="select" name="sex">
                  <option disabled value="">
                    Select Gender
                  </option>
                  {genders.map((item) => (
                    <option value={item} key={item}>
                      {item}
                    </option>
                  ))}
                </Field>
              </div>

              <div>
                <Field as="select" name="country">
                  <option disabled value="">
                    Select Country
                  </option>
                  {countries.map((item) => (
                    <option value={item} key={item}>
                      {item}
                    </option>
                  ))}
                </Field>
              </div>

              <div>
                <Field as="select" name="year">
                  <option disabled value="">
                    Select Year
                  </option>
                  {Array(20)
                    .fill(0)
                    .map((_, index) => new Date().getFullYear() + index)
                    .map((item) => (
                      <option value={item} key={item}>
                        {item}
                      </option>
                    ))}
                </Field>
              </div>
              <button type="submit">Predict</button>
            </Form>
          </Formik>
        </div>
        <div className={styles.resultContainer}>
          <img src={ChartImage} alt="chart" />
          <p>
            <b>Result:</b> {result} %
          </p>
        </div>
      </div>
    </div>
  );
}

export default UnemploymentRatePredictorSection;
