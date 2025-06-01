import os
from datetime import datetime
from airtable import Airtable

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Valuations")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

def log_valuation(
    postcode=None,
    ai_estimate=None,
    floor_area=None,
    epc_rating=None,
    heating_type=None,
    bedrooms=None,
    bathrooms=None,
    confidence_score=None,
    user_email=None,
    source=None,
    notes=None
):
    record = {
        "Postcode": postcode,
        "AI Estimate": ai_estimate,
        "EPC Rating": epc_rating,
        "Heating Type": heating_type,
        "Floor Area": floor_area,
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Confidence": confidence_score,
        "Email": user_email,
        "Source": source,
        "Valuation Date": datetime.now().isoformat(),
        "Notes": notes
    }

    try:
        response = airtable.insert(record)
        print("Airtable insert response:", response)
    except Exception as e:
        print("Airtable logging failed:", e)