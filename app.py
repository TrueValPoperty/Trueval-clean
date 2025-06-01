
from flask import Flask, request, jsonify
import joblib
import os
from airtable_logger import log_valuation
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TRAIN_API_TOKEN")
model = joblib.load("ai_estimator.pkl")

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to TrueVal AI Property Valuations"}), 200

@app.route('/valuation', methods=['POST'])
def valuation():
    try:
        data = request.get_json()
        features = [
            data.get("bedrooms", 0),
            data.get("bathrooms", 0),
            data.get("square_feet", 0),
            data.get("postcode", ""),
            data.get("epc_rating", ""),
            data.get("heating_type", ""),
        ]
        # Reshape and predict
        prediction = model.predict([features])[0]

        response = {
            "ai_estimate": round(prediction, 2),
            "epc_rating": data.get("epc_rating"),
            "heating_type": data.get("heating_type"),
            "confidence": "medium",
        }

        # Log to Airtable
        log_valuation({
            **data,
            "ai_estimate": response["ai_estimate"],
            "confidence": response["confidence"]
        })

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train', methods=['POST'])
def train():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    try:
        from train_model import train_and_save_model
        train_and_save_model()
        return jsonify({"message": "Model retrained successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
