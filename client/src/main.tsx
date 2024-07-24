import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import FlightSearch from "./components/Flights/FlightSearch.tsx";
// import Radius from "./components/CardInsperation.tsx/Radius.tsx";
import Geo from "./components/CardInsperation.tsx/Geo.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <div className="logo w-full text-center py-4">
  <span className="text-2xl md:text-3xl lg:text-4xl font-bold">
    FlightSpark
  </span>
</div>
    <FlightSearch />
    <Geo />

    {/* <Radius /> */}
  </React.StrictMode>
);
