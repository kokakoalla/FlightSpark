// Tämä on FlightList-komponentti, joka luo lentojen listan
import React from "react";
import FlightCard from "../Card/FlightCard";

interface Route { //Määritellään Route-interface, joka kuvaa Route-tyyppistä dataa
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

const FlightList: React.FC<FlightListProps> = ({ flights }) => ( //Määritellään FlightList-komponentti, joka saa propsina FlightListProps-tyyppistä dataa
  <div className="py-14">
    {flights.length > 0 && //Jos flight listassao n on enemmän kuin 0, niin käydään läpi jokainen lento ja luodaan niistä FlightCard-komponentti
      flights.map((flight, index) => ( //Käydään läpi jokainen lento ja luodaan niistä FlightCard-komponentti
        <div key={index}>
          <FlightCard  //Kutsutaan FlightCard-komponentti ja annetaan sille propsina Flight-tyyppistä dataa
            price={flight.price} //propsina annetaan lentojen hinta
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
