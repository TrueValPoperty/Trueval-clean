
import os
from airtable import Airtable
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

def log_valuation(data):
    try:
        record = {
            "Postcode": data.get("postcode", ""),
            "Bedrooms": data.get("bedrooms", 0),
            "Bathrooms": data.get("bathrooms", 0),
            "Square Feet": data.get("square_feet", 0),
            "EPC Rating": data.get("epc_rating", ""),
            "Heating Type": data.get("heating_type", ""),
            "AI Estimate": data.get("ai_estimate", 0),
            "Confidence": data.get("confidence", ""),
            "Email": data.get("email", "")
        }
        airtable.insert(record)
    except Exception as e:
        print("Airtable logging error:", e)
