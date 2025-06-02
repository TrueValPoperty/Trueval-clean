
from flask import Flask, request, jsonify
import joblib
import traceback
import numpy as np
import pandas as pd

app = Flask(__name__)

try:
    model = joblib.load("ai_estimator.pkl")
except Exception as e:
    print("Model load failed:", e)
    model = None

@app.route('/')
def index():
    return "TrueVal AI Property Valuation API"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    try:
        input_data = request.get_json()
        df = pd.DataFrame([input_data])
        prediction = model.predict(df)[0]
        return jsonify({'predicted_price': prediction})
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
