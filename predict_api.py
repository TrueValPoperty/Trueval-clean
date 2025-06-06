
from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("trueval_model.pkl")

epc_map = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
heating_types = ['gas', 'electric', 'oil', 'biomass', 'heat pump']

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            data = request.form
            df = pd.DataFrame([{
                "num_bedrooms": int(data["bedrooms"]),
                "num_bathrooms": int(data["bathrooms"]),
                "floor_area": float(data["sqft"]),
                "epc_rating_numeric": epc_map.get(data["epc_rating"].upper(), 4),
                **{f"heating_{ht}": int(data["heating_type"] == ht) for ht in heating_types}
            }])
            prediction = model.predict(df)[0]
            return render_template("form.html", prediction=round(prediction, 2))
        except Exception as e:
            return render_template("form.html", error=str(e))
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
