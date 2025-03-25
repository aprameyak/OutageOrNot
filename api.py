from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('power_outage_model.pkl')

@app.route('/predict', methods=['POST'])
def predict_outage():
    """
    Receives processed data, makes predictions, and returns results.
    """
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        prediction = model.predict_proba(df)[:, 1].tolist() #probability of outage.
        return jsonify({'predictions': prediction})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
