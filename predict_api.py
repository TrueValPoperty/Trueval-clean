from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("trueval_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    required_fields = ['num_bedrooms', 'num_bathrooms', 'floor_area', 'epc_rating']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing one of the required fields: {required_fields}"}), 400

    epc_map = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
    epc_numeric = epc_map.get(data['epc_rating'].upper())
    if not epc_numeric:
        return jsonify({"error": "Invalid EPC rating"}), 400

    X = np.array([[data['num_bedrooms'], data['num_bathrooms'], data['floor_area'], epc_numeric]])
    prediction = model.predict(X)[0]

    return jsonify({"estimated_price": round(prediction, 2)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
