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

        features = np.array([[data['bedrooms'], data['bathrooms'], data['sqft']]])
        prediction = model.predict(features)
        print("Prediction:", prediction)

        return jsonify({'prediction': float(prediction[0])})
    except Exception as e:
        print("Error during prediction:", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
