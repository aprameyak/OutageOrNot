import tensorflow as tf
import pickle
import requests
import numpy as np
import pandas as pd

data = requests.get('https://api.weather.gov/')

import requests

def get_nws_data(latitude, longitude):
    try:
        points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
        points_response = requests.get(points_url)
        points_response.raise_for_status()
        points_data = points_response.json()
        office = points_data['properties']['gridId']
        grid_x = points_data['properties']['gridX']
        grid_y = points_data['properties']['gridY']
        station = points_data['properties']['observationStations'][0].split('/')[-1]
        forecast_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast"
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        hourly_forecast_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast/hourly"
        hourly_forecast_response = requests.get(hourly_forecast_url)
        hourly_forecast_response.raise_for_status()
        hourly_forecast_data = hourly_forecast_response.json()
        alerts_url = f"https://api.weather.gov/alerts/active?point={latitude},{longitude}"
        alerts_response = requests.get(alerts_url)
        alerts_response.raise_for_status()
        alerts_data = alerts_response.json()


        return {
            'forecast': forecast_data,
            'hourly_forecast': hourly_forecast_data,
            'alerts': alerts_data,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving NWS data: {e}")
        return None

weather_data = get_nws_data(34.0522, -118.2437) 
if weather_data:
    print(weather_data['forecast'])