import React from "react";
import Button from "@mui/material/Button"; 
import { format } from "date-fns"; 

type CardProps = {
  title: string;
  paragraph: string;
  deep_link: string;
  price: number;
  local_departure: string;
  local_arrival: string;
  cityFrom: string;
  cityTo: string;
  airlines: string;
};

const formatTime = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

const Card = ({
  title,
  paragraph,
  deep_link,
  cityFrom,
  cityTo,
  airlines,
  price,
  local_departure,
  local_arrival,
}: CardProps) => (
  <div className="max-w-3xl mx-auto my-9 bg-white py shadow-md rounded-lg overflow-hidden">
    <div className="flex items-center justify-between px-4 py-7 border-b">
      <div className="text-lg font-bold text-blue-600">{airlines}</div>
      <div className="flex space-x-4">
        <div className="flex flex-col items-center">
          <div className="text-2xl"> {`${formatTime(local_departure)}`}</div>
          <div className="text-gray-600">{cityFrom}</div>
        </div>
        <div className="flex flex-col items-center">
          <div className="text-sm text-gray-600">2 t 55 min</div>
          <div className="text-gray-600">Suora</div>
        </div>
        <div className="flex flex-col items-center">
          <div className="text-2xl">{`${formatTime(local_arrival)}`}</div>
          <div className="text-gray-600">{cityTo}</div>
        </div>
      </div>
      <div className="flex flex-col items-center">
        <div className="text-2xl text-gray-900">{price} €</div>
        <Button
          className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          variant="contained"
          href={deep_link}
          target="_blank"
        >
          Valitse ➔
        </Button>
      </div>
    </div>
  </div>
);

export default Card;
