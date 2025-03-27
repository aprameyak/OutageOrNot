import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_relevant_nws_data(latitude, longitude):
    try:
        headers = {
            'User-Agent': '(OutageOrNot, contact@email.com)',
            'Accept': 'application/geo+json'
        }
        
        points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
        points_response = requests.get(points_url, headers=headers)
        points_response.raise_for_status()
        points_data = points_response.json()
        
        office = points_data['properties']['gridId']
        grid_x = points_data['properties']['gridX']
        grid_y = points_data['properties']['gridY']

        forecast_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast"
        forecast_response = requests.get(forecast_url, headers=headers)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        relevant_forecast = [{
            'startTime': period['startTime'],
            'endTime': period['endTime'],
            'temperature': period['temperature'],
            'windSpeed': period['windSpeed'],
            'windDirection': period['windDirection'],
            'probabilityOfPrecipitation': period['probabilityOfPrecipitation']['value'] if period['probabilityOfPrecipitation'] else None,
        } for period in forecast_data['properties']['periods']]

        hourly_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast/hourly"
        hourly_response = requests.get(hourly_url, headers=headers)
        hourly_response.raise_for_status()
        hourly_data = hourly_response.json()
        
        relevant_hourly = [{
            'startTime': period['startTime'],
            'temperature': period['temperature'],
            'windSpeed': period['windSpeed'],
            'windDirection': period['windDirection'],
            'probabilityOfPrecipitation': period['probabilityOfPrecipitation']['value'] if period['probabilityOfPrecipitation'] else None,
        } for period in hourly_data['properties']['periods']]

        alerts_url = f"https://api.weather.gov/alerts/active?point={latitude},{longitude}"
        alerts_response = requests.get(alerts_url, headers=headers)
        alerts_response.raise_for_status()
        alerts_data = alerts_response.json()
        
        relevant_alerts = [{
            'event': feature['properties']['event'],
            'severity': feature['properties']['severity'],
            'effective': feature['properties']['effective'],
            'expires': feature['properties']['expires'],
            'description': feature['properties']['description'],
        } for feature in alerts_data['features']] if alerts_data['features'] else []

        return {
            'forecast': relevant_forecast,
            'hourly_forecast': relevant_hourly,
            'alerts': relevant_alerts
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def findLocation(state):
    state_coordinates = {
        'AL': (32.7794, -86.8287), 'AK': (64.0685, -152.2782),
        'AZ': (34.2744, -111.6602), 'AR': (34.8938, -92.4426),
        'CA': (37.1841, -119.4696), 'CO': (38.9972, -105.5478),
        'CT': (41.6219, -72.7273), 'DE': (38.9896, -75.5050),
        'FL': (28.6305, -82.4497), 'GA': (32.6415, -83.4426),
        'HI': (20.2927, -156.3737), 'ID': (44.3509, -114.6130),
        'IL': (40.0417, -89.1965), 'IN': (39.8942, -86.2816),
        'IA': (42.0751, -93.4960), 'KS': (38.4937, -98.3804),
        'KY': (37.5347, -85.3021), 'LA': (31.0689, -91.9968),
        'ME': (45.3695, -69.2428), 'MD': (39.0550, -76.7909),
        'MA': (42.2596, -71.8083), 'MI': (44.3467, -85.4102),
        'MN': (46.2807, -94.3053), 'MS': (32.7364, -89.6678),
        'MO': (38.3566, -92.4580), 'MT': (47.0527, -109.6333),
        'NE': (41.5378, -99.7951), 'NV': (39.3289, -116.6312),
        'NH': (43.6805, -71.5811), 'NJ': (40.1907, -74.6728),
        'NM': (34.4071, -106.1126), 'NY': (42.9538, -75.5268),
        'NC': (35.5557, -79.3877), 'ND': (47.4501, -100.4659),
        'OH': (40.2862, -82.7937), 'OK': (35.5889, -97.4943),
        'OR': (43.9336, -120.5583), 'PA': (40.8781, -77.7996),
        'RI': (41.6762, -71.5562), 'SC': (33.9169, -80.8964),
        'SD': (44.4443, -100.2263), 'TN': (35.8580, -86.3505),
        'TX': (31.4757, -99.3312), 'UT': (39.3055, -111.6703),
        'VT': (44.0687, -72.6658), 'VA': (37.5215, -78.8537),
        'WA': (47.3826, -120.4472), 'WV': (38.6409, -80.6227),
        'WI': (44.6243, -89.9941), 'WY': (42.9957, -107.5512)
    }
    
    if state not in state_coordinates:
        raise ValueError(f"Invalid state code: {state}")
    
    return state_coordinates[state]

def getWeatherData(state):
    try:
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set")

        state = state.upper()
        latitude, longitude = findLocation(state)
        weather_data = get_relevant_nws_data(latitude, longitude)
        
        if weather_data is None:
            return {"error": "Failed to fetch weather data"}

        prompt = f"""
        Analyze the following weather data and determine if there's a risk of power outages.
        Consider these factors:
        - High winds (especially over 30mph)
        - Severe weather alerts
        - Extreme temperatures
        - Precipitation probability
        
        Weather data: {weather_data}
        
        In two words or less asses the risk of power outage with either, very unlikely, unlikely, likely, or very likely.
        """

        weather_summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a weather and power grid expert. Provide concise, accurate assessments of power outage risks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return weather_summary['choices'][0]['message']['content'].strip()
    
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": f"Error getting weather data analysis: {str(e)}"}
