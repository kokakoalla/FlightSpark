import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import SearchForm from "./SearchForm";
import FlightList from "./FlightList";

const API_BASE_URL = "http://localhost:5000/api";

interface LocationResponse {
  locations: { code: string; name: string; country: { name: string } }[];
}

interface Flight {
  local_departure: string;
  local_arrival: string;
  price: number;
  deep_link: string;
  cityFrom: string;
  cityTo: string;
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

  const fetchCities = useCallback(
    async (term: string, setter: (options: string[]) => void) => {
      if (term.length < 3) {
        setter([]);
        return;
      }
      try {
        const response = await axios.get<LocationResponse>(
          `${API_BASE_URL}/locations`,
          { params: { term } }
        );
        setter(response.data.locations.map((location) => location.name));
      } catch (error) {
        console.error("Error fetching location data:", error);
        setError("Failed to fetch location data.");
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    setLoading(true);
    fetchCities(fromCity, setFromCityOptions);
  }, [fromCity, fetchCities]);

  useEffect(() => {
    setLoading(true);
    fetchCities(toCity, setToCityOptions);
  }, [toCity, fetchCities]);

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

      const flightsWithDeeplink = response.data.data.map((flight: any) => ({
        ...flight,
        deep_link: `https://www.kiwi.com/deep?affilid=flyfindflyfind&currency=EUR&flightsId=${flight.id}&from=${fromCityCode}&lang=en&passengers=${adults}&to=${toCityCode}&booking_token=${flight.booking_token}`,
      }));

      setFlights(flightsWithDeeplink);
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
