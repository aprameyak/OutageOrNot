from flask import Flask, request, jsonify
import requests
import pandas as pd

app = Flask(__name__)

# Replace with your actual model API endpoint
MODEL_API_URL = 'http://model-api/predict'

# Replace with your historical outage data (example DataFrame)
historical_outages = pd.DataFrame({
    'timestamp': ['2023-10-26 10:00:00', '2023-10-27 15:30:00', '2023-10-28 08:00:00'],
    'location': ['Area A', 'Area B', 'Area C'],
    'duration': [2, 1, 3]
})

@app.route('/predict', methods=['POST'])
def predict_outage():
    """
    Receives weather data, sends it to the model API, and returns the prediction.
    """
    try:
        weather_data = request.get_json()

        # Send weather data to the model API
        response = requests.post(MODEL_API_URL, json=weather_data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        prediction = response.json()['prediction']

        return jsonify({'prediction': prediction})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Model API request failed: {e}'}), 500
    except KeyError:
        return jsonify({'error': 'Invalid prediction format from model API'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@app.route('/historical_outages', methods=['GET'])
def get_historical_outages():
    """
    Returns historical outage data.
    """
    try:
        # Convert DataFrame to JSON
        outages_json = historical_outages.to_json(orient='records')
        return outages_json
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
