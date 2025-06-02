from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load your trained model
model = joblib.load("ai_estimator.pkl")

@app.route("/")
def home():
    return "TrueVal backend is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    prediction = model.predict([list(data.values())])
    return jsonify({"valuation": prediction[0]})
