from flask import Flask, render_template, request, jsonify
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__)

# Load university data once
universities_df = pd.read_csv('universities.csv')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/student-score', methods=['POST'])
def student_score():
    data = request.get_json()
    lat, lon = data.get('lat'), data.get('lon')
    user_location = (lat, lon)

    universities_df['distance_km'] = universities_df.apply(
        lambda row: geodesic(user_location, (row['latitude'], row['longitude'])).km, axis=1
    )

    nearest = universities_df.sort_values('distance_km').iloc[0]
    nearest_distance = nearest['distance_km']
    score = max(0, 100 - nearest_distance)

    return jsonify({
        'nearest_university': nearest['name'],
        'nearest_distance_km': round(nearest_distance, 2),
        'student_investment_score': round(score, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
