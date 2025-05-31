from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from zoopla_client.zoopla import Zoopla

load_dotenv()

app = Flask(__name__)
zoopla = Zoopla(api_key=os.getenv('ZOOPLA_API_KEY'))

@app.route('/')
def home():
    return "Welcome to TrueVal – AI-Powered Property Valuations"

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

        return jsonify({
            "postcode": postcode,
            "valuation": f"£{int(price):,}",
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    from airtable import Airtable
import os

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

def log_valuation_to_airtable(postcode, zoopla_price):
    airtable.insert({
        'postcode': postcode,
        'zoopla_valuation': int(zoopla_price),
        'date': datetime.now().isoformat()
    })
from airtable import Airtable
from datetime import datetime
import os

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

def log_valuation(postcode, zoopla_valuation, ai_valuation=None):
    record = {
        "postcode": postcode,
        "zoopla_valuation": int(zoopla_valuation),
        "date": datetime.now().isoformat()
    }
    if ai_valuation:
        record["ai_valuation"] = int(ai_valuation)

    try:
        airtable.insert(record)
        return True
    except Exception as e:
        print(f"Airtable log failed: {e}")
        return False
from airtable import Airtable
import pandas as pd
import os

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

def fetch_data_as_dataframe():
    records = airtable.get_all()

    rows = []
    for record in records:
        fields = record.get('fields', {})
        rows.append(fields)

    df = pd.DataFrame(rows)
    return df        
