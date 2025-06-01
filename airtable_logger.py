from airtable import Airtable
import os
import pandas as pd

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

def get_training_data():
    all_records = airtable.get_all()
    records = []
    for record in all_records:
        fields = record["fields"]
        if all(k in fields for k in ("bedrooms", "latitude", "longitude", "epc_rating", "heating_type", "retrofit_readiness", "actual_price")):
            records.append({
                "bedrooms": fields["bedrooms"],
                "latitude": fields["latitude"],
                "longitude": fields["longitude"],
                "epc_rating": fields["epc_rating"],
                "heating_type": fields["heating_type"],
                "retrofit_readiness": fields["retrofit_readiness"],
                "actual_price": fields["actual_price"]
            })
    return pd.DataFrame(records)
