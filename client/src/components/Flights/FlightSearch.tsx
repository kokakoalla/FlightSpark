// Tämä on FlightSearch-komponentti, joka luo lentojen hakukentän
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import SearchForm from "./SearchForm";
import FlightList from "./FlightList";

const API_BASE_URL = "http://localhost:8000/api"; //Määritellään API_BASE_URL, joka on http://localhost:5000/api

interface LocationResponse {
  locations: { code: string; name: string; country: { name: string } }[];
}

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

const FlightSearch: React.FC = () => {
  const [fromCity, setFromCity] = useState<string>("");
  const [toCity, setToCity] = useState<string>("");
  const [date, setDate] = useState<string>("");
  const [dateBack, setDateBack] = useState<string>("");
  const [adults, setAdults] = useState<number>(1);
  const [fromCityOptions, setFromCityOptions] = useState<string[]>([]);
  const [toCityOptions, setToCityOptions] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [flights, setFlights] = useState<Flight[]>([]);

  const fetchCities = useCallback(        // Määritellään fetchCities-funktio, joka hakee kaupunkien tiedot
    async (term: string, setter: (options: string[]) => void) => {  //
      if (term.length > 2) {
        try {
          const response = await axios.get<LocationResponse>(
            `${API_BASE_URL}/locations`,
            { params: { term } }
          );
          setter(response.data.locations.map((location) => location.name));
        } catch (error) {
          console.error("Error fetching location data:", error);
          setError("Failed to fetch location data.");
        }
      }
      setLoading(false);
    },
    []
  );

  useEffect(() => {
    setLoading(true);

    fetchCities(fromCity, setFromCityOptions);
  }, [fromCity]);

  useEffect(() => {
    setLoading(true);
    fetchCities(toCity, setToCityOptions);
  }, [toCity]);

  const handleSearch = async () => {
    setError(null);

    if (!fromCity || !toCity || !date) {
      setError("Please fill in all fields.");
      return;
    }

    try {
      setLoading(true);

      const [fromCityResponse, toCityResponse] = await Promise.all([
        axios.get<LocationResponse>(`${API_BASE_URL}/locations`, {
          params: { term: fromCity },
        }),
        axios.get<LocationResponse>(`${API_BASE_URL}/locations`, {
          params: { term: toCity },
        }),
      ]);

      const fromCityCode = fromCityResponse.data.locations[0].code;
      const toCityCode = toCityResponse.data.locations[0].code;

      const response = await axios.get(`${API_BASE_URL}/flights`, {
        params: {
          from: fromCityCode,
          to: toCityCode,
          date: date,
          dateBack: dateBack,
          adults: adults,
        },
      });

      setFlights(response.data);
    } catch (error) {
      console.error("Error fetching flights:", error);
      setError("Failed to fetch flights. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <SearchForm
        fromCity={fromCity}
        toCity={toCity}
        date={date}
        dateBack={dateBack}
        adults={adults}
        fromCityOptions={fromCityOptions}
        toCityOptions={toCityOptions}
        loading={loading}
        onFromCityChange={setFromCity}
        onToCityChange={setToCity}
        onDateChange={setDate}
        onDateBackChange={setDateBack}
        onAdultsChange={setAdults}
        onSearch={handleSearch}
      />
      {error && <p style={{ color: "red" }}>{error}</p>}
      <FlightList flights={flights} />
    </div>
  );
};

export default FlightSearch;
