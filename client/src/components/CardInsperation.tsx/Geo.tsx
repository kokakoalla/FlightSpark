import React, { useState, useEffect } from "react";
import Radius from "./Radius"; // Import Radius component

const Geo = () => {
  const [location, setLocation] = useState({ latitude: null, longitude: null });
  const [error, setError] = useState(null);

  useEffect(() => {
    if ("geolocation" in navigator) {
      // Geo support?
      navigator.geolocation.getCurrentPosition(
        (position) => {
          // Geo success
          const { latitude, longitude } = position.coords;
          setLocation({ latitude, longitude });
        },
        (error) => {
          // Geo errors
          let errorMessage;
          switch (error.code) {
            case error.PERMISSION_DENIED:
              errorMessage = "User denied the request for Geolocation.";
              break;
            case error.POSITION_UNAVAILABLE:
              errorMessage = "Geo information is unavailable.";
              break;
            case error.TIMEOUT:
              errorMessage = "Timeout error.";
              break;
            default:
              errorMessage = "Unknown error.";
              break;
          }
          setError(errorMessage);
        },
        {
          enableHighAccuracy: true, // high accuracy
          timeout: 5000, // waits for 5 seconds
          maximumAge: 0, // no caching
        }
      );
    } else {
      setError("Browser doesn't support geolocation.");
    }
  }, []); // UseEffect will run one time only

  return (
    <div>
      {/* <h1>GeoLocation Example</h1> */}
      {error ? (
        <p>{error}</p>
      ) : (
        <>
          {location.latitude && location.longitude ? (
            <>
              {/* <p>
                Your location: Lat {location.latitude}, Lon {location.longitude}
              </p> */}
              <Radius
                latitude={location.latitude}
                longitude={location.longitude}
              />
            </>
          ) : (
            <p>Loading your location...</p>
          )}
        </>
      )}
    </div>
  );
};

export default Geo;
