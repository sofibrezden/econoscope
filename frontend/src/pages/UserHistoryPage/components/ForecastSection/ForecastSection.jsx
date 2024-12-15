import React, { useCallback, useEffect, useState } from "react";
import WorldIcon from "../../../../assets/icons/historyIcon.png";
import styles from "../../../UserHistoryPage/components/ForecastSection/ForecastSection.module.scss";

function ForecastSection() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);

  const getData = useCallback(async () => {
    try {
      const token = localStorage.getItem("authToken"); // Отримання токена
      if (!token) {
        throw new Error("No authentication token found.");
      }

      const response = await fetch("http://127.0.0.1:5000/api/user-history", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`, // Додавання токена у заголовок
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch user history.");
      }

      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error("Error fetching user history:", error);
      setError("User not authenticated or failed to fetch data.");
    }
  }, []);

  useEffect(() => {
    getData();
  }, [getData]);

  return (
    <div className={styles.pastForecasts}>
      <h2 className={styles.pageName}>Past Forecasts</h2>
      <table>
        <tr>
          <th>Country</th>
          <th>Age</th>
          <th>Sex</th>
          <th>Year</th>
          <th>Result</th>
          <th>Status</th>
        </tr>
        {history.reverse().map((item, index) => (
          <tr>
            <td className={styles.firstColumn}>{item.country}</td>
            <td>{item.age}</td>
            <td>{item.sex}</td>
            <td>{item.year}</td>
            <td>Result...</td>
            {/* замість stability з бекенду має повертатись item.state. Зараз для тесту stability просто міняєш або на increase, або на decrease */}
            <td className={styles["stability"]}>State...</td>
            <button className={styles.bin}>🗑</button>
          </tr>
        ))}
      </table>
      {history.length == 0 && !error && (
        <p className={styles.noHistoryMessage}>No history available</p>
      )}
      {error && <p className={styles.errorMessage}>{error}</p>}
    </div>
  );
}

export default ForecastSection;
