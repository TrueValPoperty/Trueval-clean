from airtable import Airtable
from datetime import datetime
import os

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

def log_valuation(postcode, ai_estimate, floor_area=None, epc_rating=None,
                  heating_type=None, bedrooms=None, bathrooms=None,
                  last_sold_price=None, confidence_score=None, user_email=None,
                  notes=None, source="Mock API"):
    record = {
        "Postcode": postcode,
        "AI Estimate": int(ai_estimate),
        "SqFt": int(floor_area) if floor_area else None,
        "Valuation Date": datetime.now().isoformat(),
        "Notes": notes or f"EPC: {epc_rating}, Heat: {heating_type}",
        "Source": source
    }

    if bedrooms is not None:
        record["Bedrooms"] = bedrooms
    if bathrooms is not None:
        record["Bathrooms"] = bathrooms
    if last_sold_price is not None:
        record["Last Sold Price"] = last_sold_price
    if confidence_score is not None:
        record["Confidence Score"] = confidence_score
    if user_email is not None:
        record["User Email"] = user_email

    try:
        airtable.insert(record)
        return True
    except Exception as e:
        print(f"Airtable log failed: {e}")
        return False