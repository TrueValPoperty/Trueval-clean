
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import joblib

# Dummy dataset as an example
data = {
    'bedrooms': [2, 3, 4, 5],
    'bathrooms': [1, 2, 2, 3],
    'size_sqft': [850, 1200, 1500, 2000],
    'epc_rating': ['D', 'C', 'B', 'A'],
    'heating_type': ['gas', 'electric', 'gas', 'heat pump'],
    'price': [250000, 320000, 400000, 475000]
}

df = pd.DataFrame(data)

# Convert categorical columns
df_encoded = pd.get_dummies(df, columns=['epc_rating', 'heating_type'])

# Split features and target
X = df_encoded.drop(columns=['price'])
y = df_encoded['price']

# Train the model
model = DecisionTreeRegressor()
model.fit(X, y)

# Save the model
joblib.dump(model, "ai_estimator.pkl")

print("Model trained and saved as ai_estimator.pkl")
