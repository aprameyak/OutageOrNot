import requests
import openai

def get_relevant_nws_data(latitude, longitude):
    try:
        points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
        points_data = requests.get(points_url).json()
        office = points_data['properties']['gridId']
        grid_x = points_data['properties']['gridX']
        grid_y = points_data['properties']['gridY']

        forecast_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast"
        forecast_data = requests.get(forecast_url).json()
        relevant_forecast = [{
            'startTime': period['startTime'],
            'endTime': period['endTime'],
            'temperature': period['temperature'],
            'windSpeed': period['windSpeed'],
            'windDirection': period['windDirection'],
            'probabilityOfPrecipitation': period['probabilityOfPrecipitation']['value'] if period['probabilityOfPrecipitation'] else None,
        } for period in forecast_data['properties']['periods']]

        hourly_forecast_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast/hourly"
        hourly_forecast_data = requests.get(hourly_forecast_url).json()
        relevant_hourly_forecast = [{
            'startTime': period['startTime'],
            'temperature': period['temperature'],
            'windSpeed': period['windSpeed'],
            'windDirection': period['windDirection'],
            'probabilityOfPrecipitation': period['probabilityOfPrecipitation']['value'] if period['probabilityOfPrecipitation'] else None,
        } for period in hourly_forecast_data['properties']['periods']]

        alerts_url = f"https://api.weather.gov/alerts/active?point={latitude},{longitude}"
        alerts_data = requests.get(alerts_url).json()
        relevant_alerts = [{
            'event': feature['properties']['event'],
            'severity': feature['properties']['severity'],
            'effective': feature['properties']['effective'],
            'expires': feature['properties']['expires'],
            'description': feature['properties']['description'],
        } for feature in alerts_data['features']] if alerts_data['features'] else []

        return {
            'forecast': relevant_forecast,
            'hourly_forecast': relevant_hourly_forecast,
            'alerts': relevant_alerts,
        }

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def findLocation(state):
    latitude_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Find the latitude of {state}"}
        ]
    )
    longitude_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Find the longitude of {state}"}
        ]
    )
    
    latitude = latitude_response['choices'][0]['message']['content'].strip()
    longitude = longitude_response['choices'][0]['message']['content'].strip()

    return float(latitude), float(longitude)

def getWeatherData(weather_data):
    try:
        weather_summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "user", "content": f"Will there be a power outage given these conditions: {weather_data}"}
            ],
            max_tokens=100
        )
        return weather_summary['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error getting weather data analysis: {e}")
        return None


