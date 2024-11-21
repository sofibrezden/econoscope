import { Field, Form, Formik } from "formik";
import styles from "./UnemploymentRatePredictorSection.module.scss";
import { useCallback, useEffect, useState } from "react";
import axios from "axios";
import ChartImage from "../../../assets/chart.png";
import { toast } from "react-toastify";

function UnemploymentRatePredictorSection() {
  const [data, setData] = useState({ ages: [], countries: [], sexes: [] });
  const [result, setResult] = useState("");

  const getDataRequest = useCallback(async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/form-data");
      setData(response.data);
    } catch (error) {
      toast.error("Error fetching form data");
    }
  }, []);

  useEffect(() => {
    getDataRequest();
  }, [getDataRequest]);

  const handlePrediction = useCallback(async (values) => {
    try {
      const data = await axios.post("http://localhost:5000/predict", values);
      setResult(JSON.stringify(data.data));
    } catch (error) {
      setResult("");
      toast.error("Wrong Data");
    }
  }, []);

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
                  {data.ages.map((item) => (
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
                  {data.sexes.map((item) => (
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
                  {data.countries.map((item) => (
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
            <b>Result:</b> {result}
          </p>
        </div>
      </div>
    </div>
  );
}

export default UnemploymentRatePredictorSection;
