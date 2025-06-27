# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

"""
Retrains the MavunoWatch model with weather features (precip_mm, temp_C).

• Reads cleaned yield data via src.data_cleaning.clean_data  
• Reads weather CSV (monthly), aggregates to yearly averages  
• Merges on county + year  (drops rows without weather)  
• One-hot encodes crop + crop_production_system  
• Trains RandomForestRegressor  
• Saves model -> models/trained_model.pkl  
• Saves base_year  -> models/base_year.txt
"""
print("🚀 Starting model training script...")  # <-- sanity check
 

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
from src.data_cleaning import clean_data

def train_model():
    df = clean_data("data/kenya_only.csv")

    if df.empty:
        raise ValueError("❌ No data available after preprocessing.")

    # Normalize time
    base_year = df["year"].min()
    df["year_since_start"] = df["year"] - base_year

    # One-hot encode categorical features
    cols_to_encode = []
    if "crop" in df.columns:
        cols_to_encode.append("crop")
    if "crop_production_system" in df.columns:
        cols_to_encode.append("crop_production_system")

    df_encoded = pd.get_dummies(df, columns=cols_to_encode, drop_first=True)

    # Build list of features to use
    feature_cols = ["year_since_start", "area_ha"]

    # 🔁 Add weather features if available
    if "precip_mm" in df_encoded.columns:
        feature_cols.append("precip_mm")
    if "temp_C" in df_encoded.columns:
        feature_cols.append("temp_C")

    # ➕ Add encoded crop/system features
    feature_cols += [
        col for col in df_encoded.columns 
        if col.startswith("crop_") or col.startswith("crop_production_system_")
    ]

    # Target column
    if "yield_ton_per_ha" not in df_encoded.columns:
        raise ValueError("❌ 'yield_ton_per_ha' column missing in data.")
    
    X = df_encoded[feature_cols]
    y = df_encoded["yield_ton_per_ha"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)

    print("📊 Model Evaluation:")
    print("✅ RMSE:", round(rmse, 2))
    print("✅ MAE :", round(mae, 2))

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/trained_model.pkl")
    print("✅ Model saved to models/trained_model.pkl")

    # Save base year for frontend/backend prediction normalization
    with open("models/base_year.txt", "w") as f:
        f.write(str(base_year))
    print("📦 Saved base year:", base_year)

if __name__ == "__main__":
    train_model()
