"use client";
import React, { useState } from "react";
import axios from 'axios';

export default function Home() {
  const [state, setState] = useState("");
  const [prediction, setPrediction] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onClick = async () => {
    setLoading(true);
    setPrediction("");
    setError("");

    if (!state || state.length !== 2) {
      setError("Please enter a valid 2-letter state code (e.g., CA, NY)");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post("http://localhost:5000/predict", { 
        state: state.toUpperCase() 
      });
      
      if (response.data.success) {
        setPrediction(response.data.data);
      } else {
        setError(response.data.message || "An error occurred");
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setError(error.response.data.message || "Error occurred while fetching prediction");
      } else {
        setError("Error connecting to the server");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold text-center mb-8 text-blue-400">
            Power Outage Predictor
          </h1>
          
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            <p className="text-lg text-gray-300 mb-6 text-center">
              Enter your state to get a prediction on whether there will be a power outage
            </p>

            <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
              <input 
                value={state}
                onChange={(e) => setState(e.target.value.toUpperCase())}
                placeholder="Enter state (e.g., CA)"
                className="px-4 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg 
                         focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                         placeholder-gray-400 w-full sm:w-48"
                maxLength={2}
              />
              <button 
                onClick={onClick}
                disabled={loading}
                className={`px-6 py-2 rounded-lg transition-colors w-full sm:w-auto
                          ${loading 
                            ? 'bg-gray-600 cursor-not-allowed' 
                            : 'bg-blue-500 hover:bg-blue-600 active:bg-blue-700'}`}
              >
                {loading ? 'Predicting...' : 'Predict'}
              </button>
            </div>

            {error && (
              <div className="mt-6 p-4 bg-red-900/50 border border-red-500 rounded-lg">
                <p className="text-red-300 text-center">
                  {error}
                </p>
              </div>
            )}
            
            {prediction && (
              <div className="mt-6 p-4 bg-gray-700/50 border border-gray-600 rounded-lg">
                <p className="text-gray-200 text-center whitespace-pre-line">
                  {prediction}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
