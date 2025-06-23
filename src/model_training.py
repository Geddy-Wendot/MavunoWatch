# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

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
        raise ValueError("❌ No data available after preprocessing. Check for valid numeric values.")

    # One-hot encode 'crop' and 'crop_production_system' if present
    cols_to_encode = []
    if "crop" in df.columns:
        cols_to_encode.append("crop")
    if "crop_production_system" in df.columns:
        cols_to_encode.append("crop_production_system")

    df_encoded = pd.get_dummies(df, columns=cols_to_encode, drop_first=True)

    # Define feature columns
    feature_cols = ["year", "area_ha"] + [
        col for col in df_encoded.columns 
        if col.startswith("crop_") or col.startswith("crop_production_system_")
    ]

    # Target
    X = df_encoded[feature_cols]
    y = df_encoded["yield_ton_per_ha"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)

    print("📊 Model Evaluation:")
    print("✅ RMSE:", round(rmse, 2))
    print("✅ MAE :", round(mae, 2))

    # Save model
    model_path = "models/trained_model.pkl"
    joblib.dump(model, model_path)
    print(f"✅ Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
