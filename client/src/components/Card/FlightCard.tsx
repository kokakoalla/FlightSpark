import React from "react";
import Button from "@mui/material/Button";

interface Route {
  airline: string;
  to: string;
  departure: string;
  arrival: string;
}

interface CardProps {
  price: number;
  url: string;
  fromCity: string;
  toCity: string;
  outboundRoutes: Route[];
  returnRoutes: Route[];
}

const formatTime = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString("en-GB", {
    timeZone: "UTC",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("ru-EN", {
    timeZone: "UTC",
    day: "2-digit",
    month: "2-digit",
  });
};

const FlightCard: React.FC<CardProps> = ({
  price,
  url,
  fromCity,
  toCity,
  outboundRoutes,
  returnRoutes,
}) => {
  const outboundDeparture = outboundRoutes[0]?.departure;
  const outboundArrival = outboundRoutes[outboundRoutes.length - 1]?.arrival;
  const returnDeparture =
    returnRoutes.length > 0 ? returnRoutes[0]?.departure : null;
  const returnArrival =
    returnRoutes.length > 0
      ? returnRoutes[returnRoutes.length - 1]?.arrival
      : null;

  return (
    <div className="max-w-3xl mx-auto my-9 bg-white py shadow-md rounded-lg overflow-hidden">
      <div
        className={`flex justify-around items-center px-4 py-7
        bg-gradient-to-tr 
        from-sky-200 to-sky-300 bg-opacity-20 shadow-2xl`}
      >
        <div>
          <div className="flex items-center justify-between mb-4">
            <div className="flex space-x-4">
              <div className="flex flex-col items-center">
                <div className="text-2xl">
                  {outboundDeparture && formatTime(outboundDeparture)}
                </div>
                <div className="text-gray-600">{fromCity}</div>
                <div className="text-base">
                  {outboundDeparture && formatDate(outboundDeparture)}
                </div>
              </div>
              <div className="flex flex-col items-center "></div>
              <div className="flex flex-col items-center">
                <div className="text-2xl">
                  {outboundArrival && formatTime(outboundArrival)}
                </div>
                <div className="text-gray-600">{toCity}</div>
                <div className="text-base">
                  {outboundArrival && formatDate(outboundArrival)}
                </div>
              </div>
            </div>
          </div>
          {returnRoutes.length > 0 && (
            <>
              <div className="flex items-center justify-between mb-4">
                <div className="flex space-x-4">
                  <div className="flex flex-col items-center">
                    <div className="text-2xl">
                      {returnDeparture && formatTime(returnDeparture)}
                    </div>
                    <div className="text-gray-600">{toCity}</div>
                    <div className="text-base">
                      {returnDeparture && formatDate(returnDeparture)}
                    </div>
                  </div>
                  <div className="flex flex-col items-center"></div>
                  <div className="flex flex-col items-center">
                    <div className="text-2xl">
                      {returnArrival && formatTime(returnArrival)}
                    </div>
                    <div className="text-gray-600">{fromCity}</div>
                    <div className="text-base">
                      {returnArrival && formatDate(returnArrival)}
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
        <div className="flex flex-col items-center">
          <div className="text-2xl text-gray-900 mb-4">{price} €</div>
          <Button
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            variant="contained"
            href={url}
            target="_blank"
          >
            Valitse
          </Button>
        </div>
      </div>
    </div>
  );
};

export default FlightCard;
