from flask import Flask, request, jsonify
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__)

# Load university data once
universities_df = pd.read_csv('universities.csv')

@app.route('/')
def index():
    return "TrueVal API is live."

@app.route('/student-score', methods=['POST'])
def student_score():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')

    if lat is None or lon is None:
        return jsonify({'error': 'Missing lat/lon'}), 400

    user_location = (lat, lon)

    universities_df['distance_km'] = universities_df.apply(
        lambda row: geodesic(user_location, (row['latitude'], row['longitude'])).km,
        axis=1
    )

    nearest = universities_df.sort_values('distance_km').iloc[0]
    score = max(0, 100 - nearest['distance_km'])

    return jsonify({
        'nearest_university': nearest['name'],
        'distance_km': round(nearest['distance_km'], 2),
        'student_investment_score': round(score, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
