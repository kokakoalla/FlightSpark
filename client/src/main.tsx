import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import FlightSearch from "./FlightSearch.tsx";
import Radius from "./components/CardInsperation.tsx/Radius.tsx";
import Geo from "./components/CardInsperation.tsx/Geo.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <FlightSearch />
    <Geo />

    {/* <Radius /> */}
  </React.StrictMode>
);
