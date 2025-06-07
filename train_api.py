from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

app = Flask(__name__)

# Configuration
DATA_FILE = "airtable_data.csv"
MODEL_FILE = "ai_estimator.pkl"
AUTH_TOKEN = "trueval-secret-2025"  # Set your token here

# Core training logic
def train_model():
    if not os.path.exists(DATA_FILE):
        return {"error": "Training data file not found."}, 400

    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=["price", "bedrooms", "postcode"])

    if df.empty:
        return {"error": "No valid training data available."}, 400

    df["postcode_prefix"] = df["postcode"].str.extract(r"(\w+)")
    df = pd.get_dummies(df, columns=["postcode_prefix", "heating_type", "epc_rating"], drop_first=True)

    features = df.drop(columns=["price", "postcode"])
    labels = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    joblib.dump(model, MODEL_FILE)

    return {
        "message": "Model trained successfully.",
        "mean_absolute_error": round(mae, 2),
        "data_points": len(df),
        "features": list(features.columns)
    }

# Token-protected training endpoint
@app.route("/train", methods=["POST"])
def train_endpoint():
    auth_header = request.headers.get("Authorization")
    print("🪵 Incoming auth header:", repr(auth_header))  # Full debug

    expected = f"Bearer {AUTH_TOKEN}"
    print("🧠 Expected auth header:", repr(expected))

    if not auth_header:
        print("❌ No Authorization header received.")
        return jsonify({"error": "Missing token"}), 403

    if auth_header != expected:
        print("❌ Token mismatch.")
        return jsonify({"error": "Unauthorized"}), 403

    print("✅ Token accepted.")
    result = train_model()
    return jsonify(result)
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
