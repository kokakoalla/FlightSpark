import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";

const Radius = ({ latitude, longitude }) => {
  const [searchHistory, setSearchHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSearchHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/location/radius`, {
        params: {
          latitude,
          longitude,
        },
      });
      setSearchHistory(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching search history:", error);
      setError("Failed to fetch search history. Please try again.");
      setLoading(false);
    }
  };

  useEffect(() => {
    if (latitude && longitude) {
      fetchSearchHistory();
    }
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1>Search History</h1>
      <ul>
        {Array.isArray(searchHistory) &&
          searchHistory.map((entry, index) => (
            <li key={index}>
              <h3>Flight {index + 1}</h3>
              <ul>
                {Object.entries(entry).map(([key, value]) => (
                  <li key={key}>
                    <strong>{key}: </strong>
                    {value}
                  </li>
                ))}
              </ul>
            </li>
          ))}
      </ul>
    </div>
  );
};

export default Radius;
