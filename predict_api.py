
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import csv
import os
from datetime import datetime

app = Flask(__name__)
model = joblib.load("trueval_model.pkl")

epc_map = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
heating_types = ['gas', 'electric', 'oil', 'biomass', 'heat pump']

LOG_FILE = "predictions_log.csv"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "bedrooms", "bathrooms", "sqft", "epc", "heating", "predicted_price"])

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame([{
            "num_bedrooms": data["bedrooms"],
            "num_bathrooms": data["bathrooms"],
            "floor_area": data["sqft"],
            "epc_rating_numeric": epc_map.get(data["epc_rating"].upper(), 4),
            **{f"heating_{ht}": int(data["heating_type"] == ht) for ht in heating_types}
        }])
        prediction = model.predict(df)[0]

        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(), data["bedrooms"], data["bathrooms"],
                             data["sqft"], data["epc_rating"], data["heating_type"], round(prediction, 2)])

        return jsonify({"valuation": round(prediction, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
