
import pandas as pd
from airtable_to_dataframe import get_training_data

def prepare_training_dataset():
    df = get_training_data()

    # Drop incomplete records
    df = df.dropna(subset=["EPC", "Bedrooms", "SqFt", "Heating Type", "AI Estimate"])

    # Map EPC A–G to numeric
    epc_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    df["EPC_score"] = df["EPC"].map(epc_map)

    # Encode heating type
    df["Heating"] = df["Heating Type"].astype("category").cat.codes

    # Extract numeric region signal from postcode
    df["Region"] = df["Postcode"].apply(lambda x: int(x[-1]) if isinstance(x, str) and x[-1].isdigit() else 0)

    # Final dataset
    X = df[["EPC_score", "Bedrooms", "SqFt", "Heating", "Region"]]
    y = df["AI Estimate"]
    final = X.copy()
    final["Target Price"] = y

    # Save
    final.to_csv("training_data.csv", index=False)
    print(f"✅ Saved: {len(final)} rows to training_data.csv")

if __name__ == "__main__":
    prepare_training_dataset()
