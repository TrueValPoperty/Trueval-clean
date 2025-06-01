from flask import Flask, request, render_template, jsonify
from airtable_logger import get_training_data
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import joblib
import os

app = Flask(__name__)

API_TOKEN = os.getenv("TRAIN_API_TOKEN")

@app.route("/train", methods=["POST"])
def train_model():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    if token != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        df = get_training_data()
    except Exception as e:
        return jsonify({"error": f"Failed to fetch Airtable data: {e}"}), 500

    try:
        df["epc_rating"] = df["epc_rating"].astype("category").cat.codes
        df["heating_type"] = df["heating_type"].astype("category").cat.codes
        X = df[["bedrooms", "latitude", "longitude", "epc_rating", "heating_type", "retrofit_readiness"]]
        y = df["actual_price"]
        model = DecisionTreeRegressor()
        model.fit(X, y)
        joblib.dump(model, "ai_estimator.pkl")
        return jsonify({"status": "Training successful", "rows": len(df)}), 200
    except Exception as e:
        return jsonify({"error": f"Training failed: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
