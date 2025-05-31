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
