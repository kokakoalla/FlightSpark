import React, { useState } from "react";
import GeoLocationComponent from "./Geo";
import Radius from "./Radius";

const App = () => {
  const [location, setLocation] = useState({ latitude: null, longitude: null });

  const handleLocationRetrieved = ({ latitude, longitude }) => {
    setLocation({ latitude, longitude });
  };

  return (
    <div>
      <GeoLocationComponent onLocationRetrieved={handleLocationRetrieved} />
      {location.latitude && location.longitude ? (
        <Radius latitude={location.latitude} longitude={location.longitude} />
      ) : (
        <p>Loading your location...</p>
      )}
    </div>
  );
};

export default App;
