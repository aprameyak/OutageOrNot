from flask import Flask, request, jsonify
from model import getWeatherData

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_outage():
    try:
        data = request.get_json()
        
        if not data or 'state' not in data:
            return jsonify({'error': 'Please provide a state in the request body'}), 400
        
        state = data['state']
        
        result = getWeatherData(state)
        
        if isinstance(result, dict) and 'error' in result:
            return jsonify({'error': result['error']}), 500
            
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
