import React, { useEffect, useState, useRef } from "react";
import axios from "axios";

interface LocationProps {
  onLocationChange: (
    location: { latitude: number; longitude: number } | null
  ) => void;
}

const Location: React.FC<LocationProps> = ({ onLocationChange }) => {
  const [location, setLocation] = useState<{
    latitude: number;
    longitude: number;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const sentRef = useRef<boolean>(false); // useRef check if location been send

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const loc = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          };
          setLocation(loc);
          onLocationChange(loc);

          if (!sentRef.current) {
            // check if location was send
            // send location to flask back
            console.log("Sending location to backend:", loc);
            axios
              .post("http://localhost:5000/api/location", loc)
              .then((response) => {
                console.log("Location sent successfully:", response.data);
                sentRef.current = true; // set to true after location is sent
              })
              .catch((error) => {
                console.error("Error sending location:", error);
              });
          }
        },
        (err) => {
          setError(err.message);
          onLocationChange(null);
        }
      );
    } else {
      setError("Geolocation is not supported by this browser.");
      onLocationChange(null);
    }
  }, []); // useEffect will run one time only

  return (
    <div>
      {error && <p>Error: {error}</p>}
      {location ? (
        <p>
          Latitude: {location.latitude}, Longitude: {location.longitude}
        </p>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Location;
