import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import FlightSearch from "./components/Flights/FlightSearch.tsx";
// import Radius from "./components/CardInsperation.tsx/Radius.tsx";
import Geo from "./components/CardInsperation.tsx/Geo.tsx";
import logo from "./assets/Spark.png";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <div className=" w-full flex justify-center py-4">
      <div className="logo text-4xl">
        <img className="absolute w-24 -mt-4 mr-8" src={logo} />
        FlightSpark
      </div>
    </div>
    <FlightSearch />
    <Geo />

    {/* <Radius /> */}
  </React.StrictMode>
);
