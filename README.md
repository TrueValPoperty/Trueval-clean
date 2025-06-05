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

```
Trueval-clean/
├── app.py                  # Flask app with HTML form
├── predict_api.py         # REST API endpoint for /predict
├── train_model.py         # AI model training script
├── trueval_model.pkl      # Trained ML model
├── trueval_data.csv       # Sample dataset
├── requirements.txt       # Python dependencies
└── templates/             # HTML templates
    ├── form.html
    ├── map.html
    └── pdf_template.html
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/trueval-clean.git
cd trueval-clean
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the model (if not already trained)
```bash
python train_model.py
```

### 5. Start the API server
```bash
python predict_api.py
```

---

## 📬 API Usage

### `POST /predict`
Send JSON data like:
```json
{
  "bedrooms": 3,
  "bathrooms": 1,
  "sqft": 950,
  "postcode": "TR12",
  "epc_rating": "D"
}
```

### Sample curl
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"bedrooms": 3, "bathrooms": 1, "sqft": 950, "postcode": "TR12", "epc_rating": "D"}'
```

---

## 📄 License

MIT License – © 2025 William Tyler-Street / TrueVal

---

## 💬 Questions or Contributions?

## Contact

Open an issue or reach out via email:

- William Tyler-Street: [williamtylerstreet@gmail.com](mailto:williamtylerstreet@gmail.com)  
- TrueVal Support: [hello@trueval.co.uk](mailto:hello@trueval.co.uk)
