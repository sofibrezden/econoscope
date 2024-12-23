import {Form, Formik} from "formik";
import styles from "./UnemploymentRatePredictorSection.module.scss";
import {useCallback, useEffect, useState} from "react";
import axios from "axios";
import {toast} from "react-toastify";
import yearly_data from "../../data/yearly_unemployment_data.csv";
import {parse} from "papaparse";
import React from "react";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from "recharts";
import {Spin} from "antd";
import 'antd/dist/reset.css';
import CustomSelect from "./CustomSelect/CustomSelect";
import {API_BASE_URL} from "../../../config";
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
    const [result, setResult] = useState(null);
    const [state, setState] = useState(null);
    const [year, setYear] = useState(null);
    const [hasPrediction, setHasPrediction] = useState(false);

    useEffect(() => {
        setLoading(true);
        fetch(yearly_data)
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
                    year: item["Year"] ? item["Year"].trim() : "",
                    country: item["Country"] ? item["Country"].trim() : "",
                    gender: item["Sex"] ? item["Sex"].trim() : "",
                    age: item["Age"] ? item["Age"].trim() : "",
                    UnemploymentRate: item["Unemployment Rate (%)"]
                        ? parseFloat(item["Unemployment Rate (%)"]) * 100
                        : 0,
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
            .get(`${API_BASE_URL}/form-data`, {
                headers: {
                    'ngrok-skip-browser-warning': 'true'
                }
            })
            .then((response) => {
                console.log("Response from API:", response);  // Логування відповіді
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
            const response = await axios.post(`${API_BASE_URL}/prepare-predict`, values);
            console.log(response)
            const predictionValue = response.data.prediction * 100;
            const predictionState = response.data.state;
            const predictionYear = response.data.year;
            setResult(predictionValue.toFixed(2));
            setState(predictionState);
            setYear(predictionYear);
            handleSavePrediction(response.data);
            setFilters({
                country: values.country,
                gender: values.sex,
                age: values.age,
                year: values.year,
            });
            setHasPrediction(true);
        } catch (error) {
            setResult(null);
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
                `${API_BASE_URL}/save-prediction`,
                {
                    prediction: predictionData.prediction,
                    country: predictionData.country,
                    age: predictionData.age,
                    sex: predictionData.sex,
                    year: predictionData.year,
                    state: predictionData.state,
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
                (filters.age === "All" || item.age === filters.age) &&
                (!filters.year || parseInt(item.year) <= parseInt(filters.year))
            );
        });
        return filteredData;
    };

    const filteredData = filterData();

    const startYear = 2014;
    const endYear = 2024;

    const placeholderData = Array.from({length: parseInt(filters.year || endYear) - startYear + 1}, (_, index) => {
        const year = startYear + index;
        return {
            year: year.toString(),
            UnemploymentRate: null,
        };
    });

    const chartTitle = hasPrediction
        ? `Unemployment rate: ${filters.country !== "All" ? filters.country : "All Countries"} 
           , ${filters.age !== "All" ? filters.age : "All Ages"} 
            , ${filters.gender !== "All" ? filters.gender : "All Genders"} 
           , from 2014 to ${filters.year !== "All" ? filters.year : "All years"} years `
        : "";

    return (
        <div className={styles.container}>
            <h1 className={styles.sectionTitle}>Unemployment Rate Predictor</h1>
            <div>
                <div className={styles.formContainer}>
                    <h3 className={styles.formTitle}>Forecasting Prediction Form</h3>
                    <Formik initialValues={{age: "", sex: "", country: "", year: ""}} onSubmit={handlePrediction}>
                        {({values, setFieldValue}) => (
                            <Form className={styles.inputContainer}>
                                <div>
                                    <CustomSelect
                                        placeholder="Select Age"
                                        options={ages.map(age => ({value: age, label: age.toString()}))}
                                        value={values.age ? {value: values.age, label: values.age.toString()} : null}
                                        onChange={(value) => setFieldValue("age", value.value)}
                                    />
                                </div>
                                <div>
                                    <CustomSelect
                                        placeholder="Select Gender"
                                        options={genders.map(gender => ({value: gender, label: gender}))}
                                        value={values.sex ? {value: values.sex, label: values.sex} : null}
                                        onChange={(value) => setFieldValue("sex", value.value)}
                                    />
                                </div>
                                <div>
                                    <CustomSelect
                                        placeholder="Select Country"
                                        options={countries.map(country => ({value: country, label: country}))}
                                        value={values.country ? {value: values.country, label: values.country} : null}
                                        onChange={(value) => setFieldValue("country", value.value)}
                                    />
                                </div>
                                <div>
                                    <CustomSelect
                                        placeholder="Select Year"
                                        options={Array.from({length: 4}, (_, i) => new Date().getFullYear() + i).map(year => ({
                                            value: year,
                                            label: year.toString()
                                        }))}
                                        value={values.year ? {value: values.year, label: values.year.toString()} : null}
                                        onChange={(value) => setFieldValue("year", value.value)}
                                    />
                                </div>
                                <button type="submit" className={styles.submitButton}>
                                    Predict
                                </button>
                            </Form>
                        )}
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
                                <XAxis dataKey="year" className={styles.customAxis}
                                       label={{value: 'Year', position: 'middle', dy: 20}}/>

                                <YAxis domain={[0, 100]} className={styles.customAxis} label={{
                                    value: 'Unemployment Rate (%)',
                                    angle: -90,
                                    position: 'middle',
                                    dx: -20
                                }}/>

                                <Tooltip
                                    content={({active, payload}) => {
                                        if (active && payload && payload.length) {
                                            const year = payload[0].payload.year;
                                            const rate = payload[0].value ? payload[0].value.toFixed(2) : 'N/A';
                                            const isPredicted = year >= "2024";
                                            return (
                                                <div className={styles.customTooltip}>
                                                    <p style={{fontSize: '21px', margin: '8px 0'}}>{`Year: ${year}`}</p>
                                                    <p style={{
                                                        fontSize: '18px',
                                                        margin: '8px 0'
                                                    }}>{`Unemployment Rate: ${rate}%`}</p>
                                                    {isPredicted && (
                                                        <p style={{
                                                            color: 'red',
                                                            fontSize: '13px',
                                                            margin: '8px 0',
                                                            fontWeight: 'bold'
                                                        }}>
                                                            Predicted
                                                        </p>
                                                    )}
                                                </div>
                                            );
                                        }
                                        return null;
                                    }}
                                />

                                <Legend
                                    content={() => (
                                        <div style={{
                                            display: 'flex',
                                            justifyContent: 'center',
                                            marginTop: '30px',
                                            fontSize: '12px'
                                        }}>
                                            <div style={{display: 'flex', alignItems: 'center', marginRight: '20px'}}>
                                                <div
                                                    style={{
                                                        width: '10px',
                                                        height: '10px',
                                                        backgroundColor: '#627254',
                                                        borderRadius: '50%',
                                                        marginRight: '5px',
                                                    }}
                                                ></div>
                                                <span>Actual Data</span>
                                            </div>
                                            <div style={{display: 'flex', alignItems: 'center'}}>
                                                <div
                                                    style={{
                                                        width: '10px',
                                                        height: '10px',
                                                        backgroundColor: '#FF0000',
                                                        borderRadius: '50%',
                                                        marginRight: '5px',
                                                    }}
                                                ></div>
                                                <span>Predicted Data</span>
                                            </div>
                                        </div>
                                    )}
                                />
                                {
                                    hasPrediction && filteredData.length > 0 && (
                                        <Line
                                            type="monotone"
                                            dataKey="UnemploymentRate"
                                            stroke="#627254"
                                            strokeWidth={3}
                                            dot={(dotProps) => {
                                                const {cx, cy, payload} = dotProps;
                                                return (
                                                    <circle
                                                        cx={cx}
                                                        cy={cy}
                                                        r={4}
                                                        fill={payload.year >= "2024" ? "#FF0000" : "#627254"}
                                                        stroke={payload.year >= "2024" ? "#FF0000" : "#627254"}
                                                    />
                                                );
                                            }}
                                            activeDot={{r: 6}}
                                            strokeDasharray={(data) =>
                                                data.year >= "2024" ? "3 3" : "0"
                                            }
                                        />
                                    )
                                }
                            </LineChart>
                        </ResponsiveContainer>


                        {result !== null && (
                            <>
                                <p style={{
                                    color: '#627254',
                                    fontWeight: 'bold',
                                    marginTop: '10px',
                                    fontSize: '18px'
                                }}>
                                    <b>Result:</b> {result} %
                                </p>
                            </>
                        )}
                        {state !== null && year !== null && (
                            <>
                                <p style={{
                                    color: '#627254',
                                    marginTop: '1px',
                                    fontSize: '17px'
                                }}>
                                    Compared to the year 2023, a <u>{state.toString().toLowerCase()} </u>
                                    in the unemployment rate is expected in {year}.
                                </p>
                            </>

                        )}


                    </div>
                )}
            </div>
        </div>
    )
        ;
};

export default UnemploymentRatePredictorSection;
