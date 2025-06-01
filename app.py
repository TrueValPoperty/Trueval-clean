from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from datetime import datetime

from mock_zoopla import Zoopla
from airtable_logger import log_valuation
from epc_client import fetch_epc_data

load_dotenv()
app = Flask(__name__)
zoopla = Zoopla(api_key=os.getenv("ZOOPLA_API_KEY"))

def determine_retrofit_ready(epc, heating_type, floor_area):
    if epc in ["D", "E", "F", "G"] and heating_type == "Gas" and floor_area and floor_area > 70:
        return True
    return False

@app.route('/')
def home():
    return "Welcome to TrueVal – AI-Powered Valuations + Retrofit Readiness"

@app.route('/valuation', methods=['POST'])
def valuation():
    data = request.get_json()
    postcode = data.get('postcode', '').strip().upper()
    if not postcode:
        return jsonify({"error": "Postcode is required"}), 400

    try:
        result = zoopla.average_area_sold_price({'area': postcode})
        price = result.get('average_sold_price_5year') or result.get('average_sold_price')

        if not price:
            return jsonify({"error": "No valuation data available"}), 404

        epc_data = fetch_epc_data(postcode)
        epc_rating = epc_data.get("current-energy-rating") if epc_data else None
        heating_type = epc_data.get("mainheat-description") if epc_data else None
        floor_area = float(epc_data.get("total-floor-area", 0)) if epc_data else None

        retrofit_ready = determine_retrofit_ready(epc_rating, heating_type, floor_area)

        log_valuation(
            postcode=postcode,
            zoopla_valuation=price,
            ai_valuation=None,
            epc_rating=epc_rating,
            heating_type=heating_type,
            floor_area=floor_area,
            retrofit_ready=retrofit_ready
        )

        return jsonify({
            "postcode": postcode,
            "valuation": f"£{int(price):,}",
            "epc_rating": epc_rating,
            "heating_type": heating_type,
            "floor_area_m2": floor_area,
            "retrofit_ready": retrofit_ready,
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
