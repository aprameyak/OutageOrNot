from flask import Flask, request, jsonify
from flask_cors import CORS
from model import getWeatherData
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(handler)

def validate_state(state):
    if not isinstance(state, str):
        return False
    if len(state) != 2:
        return False
    return state.isalpha()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict_outage():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        
        if not data:
            app.logger.error("No data provided in request")
            return jsonify({
                'error': 'No data provided',
                'message': 'Please provide a request body'
            }), 400
        
        if 'state' not in data:
            app.logger.error("No state field in request data")
            return jsonify({
                'error': 'Missing field',
                'message': 'Please provide a state in the request body'
            }), 400
        
        state = data['state'].upper()
        
        if not validate_state(state):
            app.logger.error(f"Invalid state format: {state}")
            return jsonify({
                'error': 'Invalid input',
                'message': 'State must be a 2-letter code (e.g., CA, NY)'
            }), 400
        
        app.logger.info(f"Processing prediction request for state: {state}")
        result = getWeatherData(state)
        
        if isinstance(result, dict) and 'error' in result:
            app.logger.error(f"Error in weather data: {result['error']}")
            return jsonify({
                'error': 'Processing error',
                'message': result['error']
            }), 500
            
        app.logger.info(f"Successfully processed prediction for state: {state}")
        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': f'An unexpected error occurred: {str(e)}'
        }), 500

def create_app():
    return app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.logger.info(f"Starting server on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
