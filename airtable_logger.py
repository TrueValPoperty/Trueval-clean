# airtable_logger.py

import os
from airtable import Airtable

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

def log_valuation(data):
    try:
        airtable.insert(data)
    except Exception as e:
        # Log the error if Airtable insert fails
        print("Airtable logging error:", e)
