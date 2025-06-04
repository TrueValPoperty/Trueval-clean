
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

USE_DUMMY_DATA = False  # Change to True to run on dummy dataset

def train_model(X, y, model_type='linear'):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == 'tree':
        model = DecisionTreeRegressor()
        model_file = 'ai_estimator.pkl'
    else:
        model = LinearRegression()
        model_file = 'trueval_model.pkl'

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\nModel Evaluation Metrics:")
    print(f"R² Score: {r2_score(y_test, y_pred):.3f}")
    print(f"Mean Absolute Error: £{mean_absolute_error(y_test, y_pred):,.0f}")
    print(f"RMSE: £{mean_squared_error(y_test, y_pred, squared=False):,.0f}")

    joblib.dump(model, model_file)
    print(f"\n✅ Model saved as {model_file}")

# === Option 1: Use Dummy Data ===
if USE_DUMMY_DATA:
    data = {
        'bedrooms': [2, 3, 4, 5],
        'bathrooms': [1, 2, 2, 3],
        'size_sqft': [850, 1200, 1500, 2000],
        'epc_rating': ['D', 'C', 'B', 'A'],
        'heating_type': ['gas', 'electric', 'gas', 'heat pump'],
        'price': [250000, 320000, 400000, 475000]
    }
    df = pd.DataFrame(data)
    df = pd.get_dummies(df, columns=['epc_rating', 'heating_type'])
    X = df.drop(columns=['price'])
    y = df['price']
    train_model(X, y, model_type='tree')

# === Option 2: Use Real Dataset ===
else:
    DATA_FILE = 'trueval_data.csv'
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"❌ Missing {DATA_FILE}. Please provide it in the project directory.")

    df = pd.read_csv(DATA_FILE)
    epc_map = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
    df['epc_rating_numeric'] = df['epc_rating'].map(epc_map)

    df = df.dropna(subset=['sale_price', 'num_bedrooms', 'num_bathrooms', 'floor_area', 'epc_rating_numeric'])
    X = df[['num_bedrooms', 'num_bathrooms', 'floor_area', 'epc_rating_numeric']]
    y = df['sale_price']
    train_model(X, y, model_type='linear')
