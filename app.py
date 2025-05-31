from dotenv import load_dotenv
import os
from zoopla import Zoopla
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Flask on Render!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render sets PORT as an environment variable
    app.run(host='0.0.0.0', port=port)
from flask import request, jsonify

@app.route('/valuation', methods=['POST'])
def valuation():
    data = request.get_json()
    postcode = data.get('postcode')

    # Example dummy response
    return jsonify({
        "postcode": postcode,
        "valuation": "£295,000"
    })
from flask import request, jsonify

@app.route('/valuation', methods=['POST'])
def valuation():
    try:
        data = request.get_json()
        postcode = data.get('postcode', '').strip()

        if not postcode:
            return jsonify({"error": "Postcode is required"}), 400

        # Placeholder: Replace with your AI model or valuation logic
        mock_valuation = "£285,000"  # You can later integrate ML or DB lookup here

        return jsonify({
            "postcode": postcode,
            "valuation": mock_valuation,
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
