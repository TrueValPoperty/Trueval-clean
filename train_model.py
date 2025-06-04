
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import numpy as np

# === Load and prepare data ===
DATA_FILE = 'trueval_data.csv'

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Expected {DATA_FILE} in project root. Please add your dataset.")

# Load dataset
df = pd.read_csv(DATA_FILE)

# Convert EPC ratings to numeric scale
epc_map = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
df['epc_rating_numeric'] = df['epc_rating'].map(epc_map)

# Drop rows with missing values
df = df.dropna(subset=['sale_price', 'num_bedrooms', 'num_bathrooms', 'floor_area', 'epc_rating_numeric'])

# Define input features and target
features = ['num_bedrooms', 'num_bathrooms', 'floor_area', 'epc_rating_numeric']
X = df[features]
y = df['sale_price']

# === Split and train ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# === Evaluate ===
y_pred = model.predict(X_test)

print("Model Evaluation Metrics:")
print(f"R² Score: {r2_score(y_test, y_pred):.3f}")
print(f"Mean Absolute Error: £{mean_absolute_error(y_test, y_pred):,.0f}")
print(f"Root Mean Squared Error: £{np.sqrt(mean_squared_error(y_test, y_pred)):,.0f}")

# === Save model ===
MODEL_PATH = 'trueval_model.pkl'
joblib.dump(model, MODEL_PATH)
print(f"\nModel saved to: {MODEL_PATH}")
