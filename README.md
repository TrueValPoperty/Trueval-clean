# TrueVal – AI Property Valuation API

**TrueVal** is a lightweight AI-powered property valuation platform. It enables users to submit property data via a simple web form or API and receive real-time valuation predictions based on trained machine learning models.

## 🚀 Features

- 🔁 AI-powered property valuation with trained `LinearRegression` model
- 📬 RESTful `/predict` endpoint for automated estimates
- 🌐 Web form interface for manual input
- 🗺️ Map integration for property browsing (Leaflet-ready)
- 📄 PDF template support for printable reports
- 🔐 Ready for deployment to services like Render

---

## 🧱 Project Structure

Trueval-clean/
├── app.py # Flask app with HTML form
├── predict_api.py # REST API endpoint for /predict
├── train_model.py # AI model training script
├── trueval_model.pkl # Trained ML model
├── trueval_data.csv # Sample dataset
├── requirements.txt # Python dependencies
└── templates/ # HTML templates
├── form.html
├── map.html
└── pdf_template.html

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/trueval-clean.git
cd trueval-clean
