import os
import pandas as pd
from airtable import Airtable

def get_training_data():
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME", "Valuations")
    api_key = os.getenv("AIRTABLE_API_KEY")

    airtable = Airtable(base_id, table_name, api_key)
    records = airtable.get_all()

    rows = []
    for record in records:
        fields = record.get("fields", {})
        if "AI Estimate" in fields:
            rows.append({
                "Postcode": fields.get("Postcode"),
                "EPC": fields.get("EPC Rating"),
                "Bedrooms": fields.get("Bedrooms"),
                "SqFt": fields.get("Floor Area"),
                "Heating Type": fields.get("Heating Type"),
                "AI Estimate": fields.get("AI Estimate")
            })

    return pd.DataFrame(rows)