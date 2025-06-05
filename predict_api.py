import numpy as np
from flask import Flask, request, jsonify
import joblib
import traceback

app = Flask(__name__)
model = joblib.load("trueval_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)

        epc_map = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
        epc_numeric = epc_map.get(str(data.get('epc_rating', '')).upper(), 0)

        features = np.array([[
            data['bedrooms'],
            data['bathrooms'],
            data['sqft'],
            epc_numeric
        ]])
        prediction = model.predict(features)
        print("Prediction:", prediction)

        return jsonify({'prediction': float(prediction[0])})
    except Exception as e:
        print("Error during prediction:", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
