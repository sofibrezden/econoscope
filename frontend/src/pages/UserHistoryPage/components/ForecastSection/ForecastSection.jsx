import React, {useCallback, useEffect, useState} from "react";
import WorldIcon from "../../../../assets/icons/historyIcon.png";
import styles from "../../../UserHistoryPage/components/ForecastSection/ForecastSection.module.scss";

function ForecastSection() {
    const [history, setHistory] = useState([]);
    const [error, setError] = useState(null);

    const getData = useCallback(async () => {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/user-history", {
                    method: "GET",
                    credentials: "include",
                });
                const data = await response.json();
                setHistory(data);
            } catch (error) {
                console.error("Error fetching user history:", error);
                setError("User not authenticated or failed to fetch data.");
            }
        },
        []
    );

    useEffect(() => {
        getData();
    }, [getData]);

    return (
        <div className={styles.pastForecasts}>
            <h2 className={styles.pageName}>Past Forecasts</h2>
            {history.length > 0 ? (
                <ul className={styles.forecastList}>
                    {history.reverse().map((item, index) => (
                        <li key={index} className={styles.forecastItem}>
                            <div className={styles.forecastIcon}>
                                <img src={WorldIcon} alt="World Icon"/>
                            </div>
                            <div className={styles.forecastDetails}>
                                <h3 className={styles.countryName}>{item.country}</h3>
                                <h5 className={styles.forecastInfo}>
                                    {item.age}, {item.sex}, {item.year}
                                </h5>
                            </div>
                        </li>
                    ))}
                </ul>
            ) : (
                !error && <p className={styles.noHistoryMessage}>No history available</p>
            )}
        </div>
    );

}

export default ForecastSection
