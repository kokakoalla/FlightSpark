import React from "react";

interface CardProps {
  price: number;
  from: string;
  to: string;
  deepLink: string;
}

const Card: React.FC<CardProps> = ({ price, from, to, deepLink }) => {
  return (
    <div className="bg-primary shadow-md rounded-lg p-6 m-4">
      <p className="text-lg text-center font-bold mb-2">
        {from} - {to}
      </p>
      <p className="text-gray-700 text-center">Hinta alk. {price} €</p>
      <a
        href={deepLink}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-500 hover:underline mt-4 inline-block text-center w-full bg-white py-2 rounded-lg shadow-md"
      >
        Varaa nyt
      </a>
    </div>
  );
};

export default Card;
