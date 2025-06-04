import numpy as np
from flask import Flask, request, jsonify
import joblib
import traceback

app = Flask(__name__)
model = joblib.load("trueval_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("Incoming request received.")
        data = request.get_json(force=True)
        print("Parsed data:", data)

        # Feature extraction (example, you can expand this)
        features = [[
            data.get("bedrooms", 0),
            data.get("bathrooms", 0),
            data.get("sqft", 0),
        ]]

        prediction = model.predict(features)[0]
        print("Prediction result:", prediction)

        return jsonify({'predicted_price': f'£{prediction:,.0f}'})
    except Exception as e:
        print("Error during prediction:", e)
        return jsonify({'error': str(e)})
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
