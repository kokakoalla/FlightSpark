import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import FlightSearch from "./FlightSearch.tsx";
import Radius from "./Radius.tsx";
import Geo from "./Geo.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <p> Data for developer</p>
    <p> __________________</p>

    <Geo />
    <Radius />
    <p> Data for developer</p>
    <p> __________________</p>

    <FlightSearch />
  </React.StrictMode>
);
