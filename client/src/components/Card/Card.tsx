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
};

const formatTime = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

const Card = ({
  title,
  paragraph,
  deep_link,
  price,
  local_departure,
  local_arrival,
}: CardProps) => (
  <div className="flex flex-nowrap items-center justify-center p-1">
    <div className="w-96 h-48 border border-gray-300 p-4 rounded-md mr-4">
      <h2 className="text-lg font-semibold">
        {`${formatTime(local_departure)} - ${formatTime(local_arrival)}`}
      </h2>
      <p>{paragraph}</p>
    </div>
    <div className="w-52 h-48 border border-gray-300 p-4 rounded-md flex flex-col justify-center items-center">
      <h2 className="text-lg font-semibold text-center mb-4">{title} €</h2>
      <Button
        className="mt-4"
        variant="contained"
        href={deep_link}
        target="_blank"
      >
        Buy
      </Button>
    </div>
  </div>
);

export default Card;
