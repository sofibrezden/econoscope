import {Field, Form, Formik} from "formik";
import styles from "./UnemploymentRatePredictorSection.module.scss";
import {useCallback, useEffect, useState} from "react";
import axios from "axios";
import {toast} from "react-toastify";
import df_long from "../../data/df_long.csv";
import {parse} from "papaparse";
import React from "react";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from "recharts";
import {Select, Spin} from "antd";
import 'antd/dist/reset.css';

const {Option} = Select;

const UnemploymentRatePredictorSection = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [filters, setFilters] = useState({
        country: "All",
        gender: "All",
        age: "All",
    });
    const [countries, setCountries] = useState([]);
    const [ages, setAges] = useState([]);
    const [genders, setGenders] = useState([]);
    const [result, setResult] = useState("");
    const [hasPrediction, setHasPrediction] = useState(false);

    useEffect(() => {
        setLoading(true);
        fetch(df_long)
            .then((response) => response.text())
            .then((text) => {
                parseCSV(text);
            })
            .catch((error) => console.error("Error loading CSV file", error))
            .finally(() => setLoading(false));
    }, []);

    const parseCSV = (csvString) => {
        parse(csvString, {
            header: true,
            skipEmptyLines: true,
            complete: (result) => {
                const parsedData = result.data.map((item) => ({
                    year: item.Year ? item.Year.trim() : "",
                    country: item.Country ? item.Country.trim() : "",
                    gender: item.Sex ? item.Sex.trim() : "",
                    age: item.Age ? item.Age.trim() : "",
                    UnemploymentRate: item.UnemploymentRate ? parseFloat(item.UnemploymentRate) : 0,
                }));
                setData(parsedData);
                extractCountries(parsedData);
            },
        });
    };

    const extractCountries = (parsedData) => {
        const uniqueCountries = [...new Set(parsedData.map((item) => item.country))];
        setCountries(uniqueCountries);
    };

    useEffect(() => {
        axios
            .get("http://localhost:5000/form-data")
            .then((response) => {
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
            const response = await axios.post("http://localhost:5000/prepare-predict", values);
            const predictionValue = response.data.prediction * 100;
            setResult(predictionValue.toFixed(2));
            handleSavePrediction(response.data);
            setFilters({country: values.country, gender: values.sex, age: values.age});
            setHasPrediction(true);
        } catch (error) {
            setResult("");
            toast.error("Wrong Data");
        }
    }, []);

    const handleSavePrediction = (predictionData) => {
        const token = localStorage.getItem("authToken");
        if (!token) {
            return;
        }

        axios
            .post(
                "http://localhost:5000/save-prediction",
                {
                    model: predictionData.model,
                    r_squared: predictionData.r_squared,
                    rmse: predictionData.rmse,
                    prediction: predictionData.prediction,
                    country: predictionData.country,
                    age: predictionData.age,
                    sex: predictionData.sex,
                    year: predictionData.year,
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )
            .catch((error) => {
                console.error("Error saving prediction:", error);
            });
    };

    const filterData = () => {
        if (!hasPrediction) {
            return [];
        }

        const filteredData = data.filter((item) => {
            return (
                (filters.country === "All" || item.country === filters.country) &&
                (filters.gender === "All" || item.gender === filters.gender) &&
                (filters.age === "All" || item.age === filters.age)
            );
        });
        return filteredData;
    };

    const filteredData = filterData();

    const startYear = 2014;
    const endYear = 2024;

    const placeholderData = Array.from({length: endYear - startYear + 1}, (_, index) => {
        const year = startYear + index;
        return {
            year: year.toString(),
            UnemploymentRate: null,
        };
    });

    console.log(placeholderData);


    const chartTitle = hasPrediction
        ? `Unemployment rate in ${filters.country !== "All" ? filters.country : "All Countries"} from 2014 to 2024`
        : "";

    return (
        <div className={styles.container}>
            <h1 className={styles.sectionTitle}>Unemployment Rate Predictor</h1>
            <div>
                <div className={styles.formContainer}>
                    <h3 className={styles.formTitle}>Forecasting Prediction Form</h3>
                    <Formik initialValues={{age: "", sex: "", country: "", year: ""}} onSubmit={handlePrediction}>
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
                                    {Array(4)
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
                {loading ? (
                    <Spin size="large"/>
                ) : (
                    <div className={styles.resultContainer}>
                        {hasPrediction && (
                            <h2 className={styles.chartTitle}>
                                {chartTitle}
                            </h2>
                        )}
                        <ResponsiveContainer width="100%" height={400}>
                            <LineChart
                                data={filteredData.length > 0 ? filteredData : placeholderData}
                                margin={{
                                    top: 20,
                                    right: 30,
                                    left: 20,
                                    bottom: 20,
                                }}
                                className={styles.customChart}
                            >
                                <CartesianGrid className={styles.customGrid}/>
                                <XAxis dataKey="year" className={styles.customAxis}/>
                                <YAxis domain={[0, 0.9]} className={styles.customAxis}/>
                                <Tooltip className={styles.customTooltip}/>
                                <Legend className={styles.customLegend}/>
                                {hasPrediction && filteredData.length > 0 && (
                                    <Line
                                        type="monotone"
                                        dataKey="UnemploymentRate"
                                        className={styles.customLine}
                                        stroke="#627254"
                                        strokeWidth={3}
                                        dot={{stroke: '#627254', strokeWidth: 2, r: 4}}
                                        activeDot={{r: 6}}
                                    />
                                )}
                            </LineChart>

                        </ResponsiveContainer>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UnemploymentRatePredictorSection;
