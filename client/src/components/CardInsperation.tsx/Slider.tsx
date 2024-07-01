import React, { useState } from "react";
import Card from "./Card";

const Slider = ({ searchHistory }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % searchHistory.length);
  };

  const prevSlide = () => {
    setCurrentIndex(
      (prevIndex) =>
        (prevIndex - 1 + searchHistory.length) % searchHistory.length
    );
  };

  return (
    <div className="relative w-full flex justify-center items-center">
      <button onClick={prevSlide} className="absolute left-0 p-2">
        &lt;
      </button>
      <div className="w-full overflow-hidden">
        <div
          className="flex transition-transform duration-500"
          style={{ transform: `translateX(-${currentIndex * 100}%)` }}
        >
          {searchHistory.map((entry, index) => (
            <div
              key={index}
              className="w-full flex-shrink-0"
              style={{ width: "300px" }}
            >
              <Card
                price={entry.price}
                deepLink={entry.deep_link}
                from={entry.cityFrom}
                to={entry.cityTo}
              />
            </div>
          ))}
        </div>
      </div>
      <button onClick={nextSlide} className="absolute right-0 p-2">
        &gt;
      </button>
    </div>
  );
};

export default Slider;
