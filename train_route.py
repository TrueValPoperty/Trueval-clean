from flask import Flask, jsonify
from dotenv import load_dotenv
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from airtable_to_dataframe import get_training_data

load_dotenv()

def retrain_model():
    df = get_training_data()
    df.dropna(inplace=True)

    epc_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    df["EPC_score"] = df["EPC"].map(epc_map)
    df["Region"] = df["Postcode"].apply(lambda x: int(x[-1]) if isinstance(x, str) and x[-1].isdigit() else 0)
    df["Heating"] = df["Heating Type"].astype("category").cat.codes

    features = ["EPC_score", "Bedrooms", "SqFt", "Heating", "Region"]
    X = df[features]
    y = df["AI Estimate"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, "ai_estimator.pkl")

    return f"Model trained on {len(df)} records and saved to ai_estimator.pkl"