import React from "react";

const Card = ({ price, from, to,  deepLink }) => {
  return (
    <div className="border-solid rounded-xl border-2 border-indigo-600 ">
      <h3>Price: ${price}</h3>
      <p>Departure: {from}</p>
      <p>Arrival: {to}</p>
      <a href={deepLink} target="_blank" rel="noopener noreferrer">
        Book Now
      </a>
    </div>
  );
};

export default Card;
