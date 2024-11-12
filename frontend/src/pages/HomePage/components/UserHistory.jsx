import React, { useEffect, useState } from "react";

function UserHistory() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/user-history", {
      method: "GET",
      credentials: "include", // Include credentials for cross-origin cookies
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch user history. Ensure the user is authenticated.");
        }
        return response.json();
      })
      .then((data) => {
        if (data.error) {
          throw new Error(data.error);
        }

        console.log("Fetched user history data:", data); // Вивід даних в консоль
        setHistory(data);
      })
      .catch((err) => {
        console.error("Error fetching user history:", err);
        setError("User not authenticated or failed to fetch data.");
      });
  }, []);

  return (
    <div>
      <h2>User History</h2>
      {error && <p className="error-message">{error}</p>}
      {history.length > 0 ? (
        <ul>
          {history.map((item, index) => (
            <li key={index}>
              <strong>Country:</strong> {item.country}, <strong>Year:</strong> {item.year},
              <strong> Model:</strong> {item.model}, <strong>Forecast:</strong> {item.prediction}
            </li>
          ))}
        </ul>
      ) : (
        !error && <p>No history available</p>
      )}
    </div>
  );
}

export default UserHistory;
