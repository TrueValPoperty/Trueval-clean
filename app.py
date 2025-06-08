from flask import Flask, jsonify
from flask_cors import CORS
import csv
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)

UNIVERSITIES = []

def load_universities():
    global UNIVERSITIES
    with open("universities.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            UNIVERSITIES.append({
                "name": row["name"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"])
            })

load_universities()

def nearest_university(lat, lon):
    property_coords = (lat, lon)
    closest = min(
        UNIVERSITIES,
        key=lambda uni: geodesic(property_coords, (uni["lat"], uni["lon"])).km
    )
    distance_km = geodesic(property_coords, (closest["lat"], closest["lon"])).km
    return {
        "university": closest["name"],
        "distance_km": round(distance_km, 2)
    }

@app.route("/nearest_university/<float:lat>/<float:lon>")
def get_nearest_uni(lat, lon):
    return jsonify(nearest_university(lat, lon))

if __name__ == "__main__":
    app.run(debug=True)
