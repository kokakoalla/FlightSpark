import React from "react";
import FlightCard from "../Card/Card";

interface Flight {
  local_departure: string;
  local_arrival: string;
  price: number;
  deep_link: string;
  cityFrom: string;
  cityTo: string;
}

interface FlightListProps {
  flights: Flight[];
}

const FlightList: React.FC<FlightListProps> = ({ flights }) => (
  <div className="pt-32 w-full grid grid-cols-4 gap-4 mt-8">
    {flights.length > 0 &&
      flights.map((flight, index) => (
        <div key={index}>
          <FlightCard
            title={flight.price.toString()}
            paragraph={flight.cityFrom + " - " + flight.cityTo}
            local_departure={flight.local_departure}
            local_arrival={flight.local_arrival}
            deep_link={flight.deep_link}
          />
        </div>
      ))}
  </div>
);

export default FlightList;
