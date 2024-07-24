import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import FlightSearch from "./components/Flights/FlightSearch.tsx";
// import Radius from "./components/CardInsperation.tsx/Radius.tsx";
import Geo from "./components/CardInsperation.tsx/Geo.tsx";
import logo from "./assets/Spark.png";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
<<<<<<< HEAD
    <div className=" w-full flex justify-center py-4">
      <div className="logo text-4xl">
        <img className="absolute w-24 -mt-4 mr-8" src={logo} />
        FlightSpark
      </div>
    </div>
=======
   
    <div className="logo w-full text-center py-4"> <span 
      className="text-5xl md:text-6xl lg:text-7xl xl:text-7xl font-bold">
        FlightSpark </span>
    </div>

>>>>>>> 4eb2d9614ef9ea207c4d2d4811e3c5a24236df2b
    <FlightSearch />
    <Geo />

    {/* <Radius /> */}
  </React.StrictMode>
);
