# OutageOrNot

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white&style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white&style=for-the-badge)
![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB&style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white&style=for-the-badge)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white&style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white&style=for-the-badge)

## About

**OutageOrNot** is a full-stack application that predicts power outage risk for any U.S. state using real-time weather data and AI analysis. Built with **Python, Flask, Next.js, and OpenAI**, it pulls current conditions from the National Weather Service API — wind speed, precipitation probability, temperature, and severe weather alerts — then passes them to GPT-3.5 Turbo for a plain-language risk assessment.

## Features

- State-based location lookup with a coordinates map covering all U.S. states
- Fetches live weather data from the National Weather Service API including temperature, wind, and precipitation
- AI-powered risk assessment via OpenAI GPT-3.5 Turbo based on current weather conditions
- Incorporates active severe weather alerts into the outage risk analysis
- RESTful Flask backend with CORS support and structured error handling
- Responsive Next.js frontend styled with Tailwind CSS
- TypeScript typed throughout the frontend with Axios handling API requests

## Technology Stack

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: Python, Flask
- **AI**: OpenAI GPT-3.5 Turbo
- **Data Source**: National Weather Service API
