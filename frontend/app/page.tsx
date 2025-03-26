"use client";
import React, { useState } from "react";
import axios from 'axios';

export default function Home() {
  const [location, setLocation] = useState("");
  const [prediction, setPrediction] = useState("");

  const onClick = async () => {
    try {
      const response = await axios.post("http://localhost:5000/predict", { location });
      setPrediction(response.data.prediction);
    } catch (error) {
      setPrediction("Error occurred while fetching prediction");
    }
  };

  return (
    <div>
      <h1>
        Enter your location to get a prediction on whether there will be a power outage
      </h1>
      <input 
        value={location} 
        onChange={(e) => setLocation(e.target.value)}
      />
      <button onClick={onClick}>
        Predict
      </button>
      <p>
        {prediction}
      </p>
    </div>
  );
}
