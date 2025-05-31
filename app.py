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