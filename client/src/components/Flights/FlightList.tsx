import React from "react";
import FlightCard from "../Card/Card";

interface Route {
  airline: string;
  flight_no: string;
  from: string;
  to: string;
  departure: string;
  arrival: string;
}

interface Flight {
  price: number;
  url: string;
  from: {
    city: string;
    city_code: string;
    country: string;
  };
  to: {
    city: string;
    city_code: string;
    country: string;
  };
  outbound_routes: Route[];
  return_routes: Route[];
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
            price={flight.price}
            url={flight.url}
            fromCity={flight.from.city}
            toCity={flight.to.city}
            outboundRoutes={flight.outbound_routes}
            returnRoutes={flight.return_routes}
          />
        </div>
      ))}
  </div>
);

export default FlightList;
