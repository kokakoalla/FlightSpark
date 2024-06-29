import React, { useState } from "react";
import GeoLocationComponent from "./components/CardInsperation.tsx/Geo";
import Radius from "./components/CardInsperation.tsx/Radius";

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
