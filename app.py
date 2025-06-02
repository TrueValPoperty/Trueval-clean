
from flask import Flask, request, jsonify
import joblib
import traceback

app = Flask(__name__)

try:
    model = joblib.load("ai_estimator.pkl")
except Exception as e:
    model = None
    print("Model load failed:", e)

@app.route('/')
def index():
    return jsonify(status="OK", message="TrueVal backend is running")

@app.route('/valuation', methods=['POST'])
def valuation():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        input_data = request.get_json()
        prediction = model.predict([list(input_data.values())])
        return jsonify({"valuation": prediction[0]})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True)
