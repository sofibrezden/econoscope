import React, { useCallback, useEffect, useState } from "react";
import styles from "../../../UserHistoryPage/components/ForecastSection/ForecastSection.module.scss";
import { API_BASE_URL } from "../../../../config";

function ForecastSection() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const notesPerPage = 10;

  const getData = useCallback(async () => {
    try {
      const token = localStorage.getItem("authToken");
      if (!token) throw new Error("No authentication token found.");

      const response = await fetch(`${API_BASE_URL}/api/user-history`, {
        method: "GET",
        headers: {
          "ngrok-skip-browser-warning": "true",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) throw new Error("Failed to fetch user history.");

      const data = await response.json();
      setHistory(data);
      console.log(data);
    } catch (error) {
      console.error("Error fetching user history:", error);
      setError("User not authenticated or failed to fetch data.");
    }
  }, []);

  const deletePrediction = async (predictionId) => {
    try {
      const token = localStorage.getItem("authToken");
      const response = await fetch(`${API_BASE_URL}/delete-prediction`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
          "ngrok-skip-browser-warning": "true",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prediction_id: predictionId }),
      });

      if (!response.ok) throw new Error("Failed to delete prediction.");
      setHistory((prev) => prev.filter((item) => item.id !== predictionId));
    } catch (error) {
      console.error("Error deleting prediction:", error);
      setError("Failed to delete prediction.");
    }
  };

  useEffect(() => {
    getData();
  }, [getData]);

  const indexOfLastNote = currentPage * notesPerPage;
  const indexOfFirstNote = indexOfLastNote - notesPerPage;
  const currentNotes = history.slice(indexOfFirstNote, indexOfLastNote);
  const [showTooltip, setShowTooltip] = useState(false);

  const totalPages = Math.ceil(history.length / notesPerPage);
  const nextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className={styles.pastForecasts}>
      <h2 className={styles.pageName}>Past Forecasts</h2>
      <table>
        <thead>
          <tr>
            <th>Country</th>
            <th>Age</th>
            <th>Sex</th>
            <th>Year</th>
            <th>Result</th>

            <th
              className={styles.statusColumn}
              onMouseEnter={() => setShowTooltip(true)}
              onMouseLeave={() => setShowTooltip(false)}
            >
              Status*
              {showTooltip && (
                <div className={styles.tooltip}>Compared to 2023</div>
              )}
            </th>
            <th>Action</th>
          </tr>
        </thead>
        {currentNotes.map((item) => (
          <tr key={item.id}>
            <td className={styles.firstColumn}>{item.country}</td>
            <td>{item.age}</td>
            <td>{item.sex}</td>
            <td>{item.year}</td>
            <td>{(Number(item.prediction) * 100).toFixed(2)}%</td>
            <td
              className={(() => {
                switch (item.state) {
                  case "Decline":
                    return styles.decrease;
                  case "Growth":
                    return styles.increase;
                  default:
                    return "";
                }
              })()}
            >
              {item.state}
            </td>

            <button
              className={styles.bin}
              onClick={() => deletePrediction(item.id)}
            >
              🗑
            </button>
          </tr>
        ))}
      </table>

      {}
      {totalPages > 1 && (
        <div className={styles.pagination}>
          <button
            onClick={prevPage}
            disabled={currentPage === 1}
            className={styles.pageButton}
          >
            Prev
          </button>
          <span className={styles.pageNumber}>
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={nextPage}
            disabled={currentPage === totalPages}
            className={styles.pageButton}
          >
            Next
          </button>
        </div>
      )}

      {history.length === 0 && !error && (
        <p className={styles.noHistoryMessage}>No history available</p>
      )}
      {error && <p className={styles.errorMessage}>{error}</p>}
    </div>
  );
}

export default ForecastSection;
