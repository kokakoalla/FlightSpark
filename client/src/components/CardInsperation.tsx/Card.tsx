import React from "react";

const Card = ({ price, from, to, deepLink }) => {
  return (
    <div
      className="shadow-md rounded-lg p-6 m-4 bg-gradient-to-tr 
        from-sky-200 to-sky-300 bg-opacity-20 shadow-2xl"
    >
      <p className="text-lg text-center font-bold mb-2">
        {from} - {to}
      </p>
      <p className="text-gray-700 text-center">Hinta alk. {price} €</p>
      <a
        href={deepLink}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-700 hover:underline mt-4 inline-block text-center w-full bg-gradient-to-t from-slate-100 to-slate-500 py-2 rounded-lg shadow-md"
      >
        Varaa nyt
      </a>
    </div>
  );
};

export default Card;
