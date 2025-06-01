
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os
from airtable_logger import log_valuation
from epc_client import fetch_epc_data

app = Flask(__name__)

# Load AI model
model = joblib.load("ai_estimator.pkl")

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/valuation", methods=["POST"])
def valuation():
    try:
        # Get form data
        data = request.form
        postcode = data.get("postcode")
        bedrooms = int(data.get("bedrooms"))
        property_type = data.get("property_type")
        tenure = data.get("tenure")
        email = data.get("email")

        # Fetch EPC data
        epc_data = fetch_epc_data(postcode)
        epc_rating = epc_data.get("epc_rating", "Unknown")
        heating_type = epc_data.get("heating_type", "Unknown")
        retrofit_readiness = epc_data.get("retrofit_readiness", 0.5)

        # Combine data for prediction
        features = np.array([[bedrooms, retrofit_readiness]])
        ai_estimate = float(model.predict(features)[0])

        # Confidence score logic
        confidence_score = 0.88 if epc_rating != "Unknown" else 0.6

        # Log everything to Airtable
        log_valuation({
            "Postcode": postcode,
            "Bedrooms": bedrooms,
            "Property Type": property_type,
            "Tenure": tenure,
            "Email": email,
            "AI Estimate": ai_estimate,
            "EPC Rating": epc_rating,
            "Heating Type": heating_type,
            "Retrofit Readiness": retrofit_readiness,
            "Confidence Score": confidence_score
        })

        return render_template("form.html", estimate=ai_estimate, confidence=confidence_score)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
