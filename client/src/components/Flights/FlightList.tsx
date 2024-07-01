import React from "react";
import FlightCard from "../Card/Card";

interface Flight {
  local_departure: string;
  local_arrival: string;
  price: number;
  deep_link: string;
  cityFrom: string;
  cityTo: string;
  fromId: string;
  toId: string;
  airlines: string;
}

interface FlightListProps {
  flights: Flight[];
}

const FlightList: React.FC<FlightListProps> = ({ flights }) => (
  <div className="py-14">
    {flights.length > 0 &&
      flights.map((flight, index) => (
        <div key={index}>
          <FlightCard
            price={flight.price.toString()}
            paragraph={flight.cityFrom + " - " + flight.cityTo}
            local_departure={flight.local_departure}
            local_arrival={flight.local_arrival}
            deep_link={flight.deep_link}
            cityFrom={flight.cityFrom}
            cityTo={flight.cityTo}
            airlines={flight.airlines[0]}

          />
        </div>
      ))}
  </div>
);

export default FlightList;
