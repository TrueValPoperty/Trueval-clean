from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from datetime import datetime
import joblib

from epc_client import fetch_epc_data
from airtable_logger import log_valuation

load_dotenv()
app = Flask(__name__)
model = joblib.load("ai_estimator.pkl")

def determine_retrofit_ready(epc, heating_type, floor_area):
    if epc in ["D", "E", "F", "G"] and heating_type == "Gas" and floor_area and floor_area > 70:
        return True
    return False

@app.route('/')
def home():
    return "Welcome to TrueVal – AI Property Valuations + Retrofit Readiness"

@app.route('/valuation', methods=['POST'])
def valuation():
    data = request.get_json()
    postcode = data.get('postcode', '').strip().upper()
    user_email = data.get('email')
    bedrooms = data.get('bedrooms', 3)
    bathrooms = data.get('bathrooms')

    if not postcode:
        return jsonify({"error": "Postcode is required"}), 400

    try:
        epc_data = fetch_epc_data(postcode)
        epc_rating = epc_data.get("current-energy-rating") if epc_data else "D"
        heating_type = epc_data.get("mainheat-description") if epc_data else "Gas"
        floor_area = float(epc_data.get("total-floor-area", 0)) if epc_data else 1000
        retrofit_ready = determine_retrofit_ready(epc_rating, heating_type, floor_area)

        # AI Estimate
        epc_score = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}.get(epc_rating, 4)
        region_code = int(postcode[-1]) if postcode[-1].isdigit() else 0
        heating_code = {"Gas": 0, "Electric": 1, "Oil": 2}.get(heating_type, 1)

        input_data = [[epc_score, bedrooms, floor_area, heating_code, region_code]]
        ai_estimate = model.predict(input_data)[0]

        # Log to Airtable
        log_valuation(
            postcode=postcode,
            ai_estimate=ai_estimate,
            floor_area=floor_area,
            epc_rating=epc_rating,
            heating_type=heating_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            user_email=user_email,
            confidence_score=0.9,
            notes=f"Retrofit ready: {retrofit_ready}",
            source="AI Model"
        )

        return jsonify({
            "postcode": postcode,
            "valuation": f"£{int(ai_estimate):,}",
            "epc_rating": epc_rating,
            "heating_type": heating_type,
            "floor_area_m2": floor_area,
            "retrofit_ready": retrofit_ready,
            "confidence_score": 0.9,
            "source": "AI Model",
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    from train_route import retrain_model

@app.route('/train', methods=['POST'])
def train():
    try:
        message = retrain_model()
        return jsonify({"status": "success", "message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
import os
from flask import request

API_TOKEN = os.getenv("TRAIN_API_TOKEN")

@app.route('/train', methods=['POST'])
def train():
    token = request.headers.get("Authorization")
    if token != f"Bearer {API_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    try:
        message = retrain_model()
        return jsonify({"status": "success", "message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
