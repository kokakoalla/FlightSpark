import React, { useState, useEffect } from "react";
import axios from "axios";
import Card from "./Card";

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
      setError("Failed to fetch search history.");
      setLoading(false);
    }
  };

  useEffect(() => {
    if (latitude && longitude) {
      fetchSearchHistory();
    }
  }, [latitude, longitude]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="container mx-auto">
      <h1 className="text-center text-2xl font-bold mb-4">
        Inspiration Fly
      </h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.isArray(searchHistory) &&
          searchHistory.map((entry, index) => (
            <Card
              key={index}
              price={entry.price}
              deepLink={entry.deep_link}
              from={entry.cityFrom}
              to={entry.cityTo}
            />
          ))}
      </div>
    </div>
  );
};

export default Radius;
