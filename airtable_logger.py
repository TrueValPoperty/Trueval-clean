
import os
from airtable import Airtable

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

# Debug logging
print("DEBUG - AIRTABLE_BASE_ID:", AIRTABLE_BASE_ID)
print("DEBUG - AIRTABLE_TABLE_NAME:", AIRTABLE_TABLE_NAME)
print("DEBUG - AIRTABLE_API_KEY starts with:", AIRTABLE_API_KEY[:4] if AIRTABLE_API_KEY else "None")

airtable = None
try:
    airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)
except Exception as e:
    print("Airtable instantiation error:", e)

def log_valuation(data):
    if airtable is None:
        print("Airtable not configured; skipping log")
        return
    try:
        airtable.insert(data)
    except Exception as e:
        print("Airtable logging error:", e)
