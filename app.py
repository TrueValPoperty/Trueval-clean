from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from datetime import datetime

from mock_zoopla import Zoopla  # Use mock for now
from epc_client import fetch_epc_data
from airtable_logger import log_valuation

load_dotenv()
app = Flask(__name__)
zoopla = Zoopla(api_key=os.getenv("ZOOPLA_API_KEY"))

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
    bedrooms = data.get('bedrooms')
    bathrooms = data.get('bathrooms')

    if not postcode:
        return jsonify({"error": "Postcode is required"}), 400

    try:
        # Use mock Zoopla or real one once API key arrives
        result = zoopla.average_area_sold_price({'area': postcode})
        ai_estimate = result.get('average_sold_price_5year') or result.get('average_sold_price')

        if not ai_estimate:
            return jsonify({"error": "No valuation data available"}), 404

        # Fetch EPC data
        epc_data = fetch_epc_data(postcode)
        epc_rating = epc_data.get("current-energy-rating") if epc_data else None
        heating_type = epc_data.get("mainheat-description") if epc_data else None
        floor_area = float(epc_data.get("total-floor-area", 0)) if epc_data else None
        retrofit_ready = determine_retrofit_ready(epc_rating, heating_type, floor_area)

        # Log full valuation with AI angle into Airtable
        log_valuation(
            postcode=postcode,
            ai_estimate=ai_estimate,
            floor_area=floor_area,
            epc_rating=epc_rating,
            heating_type=heating_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            user_email=user_email,
            confidence_score=0.9,  # Placeholder
            notes=f"Retrofit ready: {retrofit_ready}",
            source="Mock AI Estimate"
        )

        return jsonify({
            "postcode": postcode,
            "valuation": f"£{int(ai_estimate):,}",
            "epc_rating": epc_rating,
            "heating_type": heating_type,
            "floor_area_m2": floor_area,
            "retrofit_ready": retrofit_ready,
            "confidence_score": 0.9,
            "source": "Mock AI Estimate",
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)