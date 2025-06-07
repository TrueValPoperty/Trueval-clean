from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

app = Flask(__name__)

# Config
DATA_FILE = "airtable_data.csv"
MODEL_FILE = "ai_estimator.pkl"
AUTH_TOKEN = "your-secure-token-here"  # Replace this with your real token

# Training logic
def train_model():
    if not os.path.exists(DATA_FILE):
        return {"error": "Training data file not found."}, 400

    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=['price', 'bedrooms', 'postcode'])

    if df.empty:
        return {"error": "No valid training data available."}, 400

    df['postcode_prefix'] = df['postcode'].str.extract(r'(\w+)')
    df = pd.get_dummies(df, columns=['postcode_prefix', 'heating_type', 'epc_rating'], drop_first=True)

    features = df.drop(columns=['price', 'postcode'])
    labels = df['price']

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

# Flask endpoint
@app.route("/train", methods=["POST"])
def train_endpoint():
    token = request.headers.get("Authorization")
    if token != f"Bearer {AUTH_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 403

    result = train_model()
    return jsonify(result)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
