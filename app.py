from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import math

app = Flask(__name__)
CORS(app)

# Load university locations on startup
universities = []
with open('universities.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            universities.append({
                'name': row['University'],
                'lat': float(row['Latitude']),
                'lon': float(row['Longitude'])
            })
        except ValueError:
            continue

# Haversine formula to calculate distance in km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

@app.route('/')
def index():
    return "TrueVal API running"

@app.route('/student-score', methods=['POST'])
def student_score():
    data = request.json
    lat, lon = data.get('lat'), data.get('lon')

    if lat is None or lon is None:
        return jsonify({'error': 'Missing lat or lon'}), 400

    nearest_distance = min(
        haversine(lat, lon, uni['lat'], uni['lon']) for uni in universities
    )

    # Score: closer gets higher score (0–100)
    score = max(0, 100 - min(nearest_distance, 50) * 2)  # score drops 2 pts/km after 25km

    return jsonify({
        'nearest_distance_km': round(nearest_distance, 2),
        'student_investment_score': round(score, 1)
    })

if __name__ == '__main__':
    app.run(debug=True)
